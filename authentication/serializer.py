from django.contrib.auth import authenticate

from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed

from .models import User


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
