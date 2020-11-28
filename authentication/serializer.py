from rest_framework import serializers
from .models import User


class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        min_length=6, max_length=32, write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name',
                  'last_name', 'gender', 'age',
                  'auth_provider']

    def validate(self, attrs):
        username = attrs.get('username', '')

        if not username.isalnum():
            return serializers.ValidationError('Username should only contain alphanumeric.')

        return attrs

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)
