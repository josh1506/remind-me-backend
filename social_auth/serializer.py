from .social_auth_api import Facebook
from rest_framework import serializers
from .user_register import user_social_register


class FacebookSocialAuthSerializer(serializers.Serializer):
    auth_token = serializers.CharField()

    def validate_auth_token(self, auth_token):
        user_data = Facebook.validate(auth_token)
        try:
            user_id = user_data['id']
            email = user_data['email']
            name = user_data['name']
            provider = 'facebook'
            data = user_social_register(
                user_id=user_id, email=email, name=name, provider=provider)

            if 'error' in str(data):
                raise serializers.ValidationError(data, 401)

            else:
                return data

        except KeyError:
            raise serializers.ValidationError(
                {'error': 'Token is invalid or already expired. Please login again'}, 401)
