from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.auth import authenticate
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode

from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed

from users.models import User


class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        min_length=6, max_length=32, write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def validate(self, attrs):
        username = attrs.get('username', '')

        if not username.isalnum():
            return serializers.ValidationError('Username should only contain alphanumeric.')

        return attrs

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class UserLoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255, required=True)
    username = serializers.CharField(max_length=255, read_only=True)
    password = serializers.CharField(
        max_length=32, min_length=6, write_only=True)
    tokens = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['email', 'username', 'password', 'tokens']

    def get_tokens(self, data):
        user = User.objects.get(email=data['email'])
        return user.get_token()

    def validate(self, attrs):
        email = attrs.get('email', '')
        password = attrs.get('password', '')
        authenticated_user = authenticate(email=email, password=password)

        if authenticated_user:
            user = User.objects.get(email=authenticated_user.email)

            if not user.is_active:
                raise AuthenticationFailed(
                    'User is currently disabled. Please contact us.')

            if not user.is_verified:
                raise AuthenticationFailed(
                    "User is not activated. Please check email's inbox or spam folder for verification token.")

            data = {
                'email': user.email,
                'username': user.username,
                'tokens': user.get_token()
            }

            return data

        else:
            raise AuthenticationFailed(
                'Invalid username or password. Please try again.')


class UserRequestPasswordResetSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=255, required=True)

    class Meta:
        fields = ['email']


class UserSetNewPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(
        max_length=32, min_length=6, write_only=True)
    uidb46 = serializers.CharField(required=True, write_only=True)
    token = serializers.SerializerMethodField()

    class Meta:
        fields = ['password', 'uidb46', 'token']

    def validate(self, attrs):
        try:
            password = attrs.get('password', '')
            uidb46 = attrs.get('uidb46', '')
            token = attrs.get('token', '')

            id = force_str(urlsafe_base64_decode(uidb46))
            user = User.objects.get(id=id)

            if PasswordResetTokenGenerator().check_token(user, token):
                raise AuthenticationFailed(
                    {'error': 'Token is invalid. Please request another one'}, 401)

            user.set_password(password)
            user.save()

            return user

        except:
            raise AuthenticationFailed(
                {'error': 'Link is invalid. Please check or request another one'}, 401)
