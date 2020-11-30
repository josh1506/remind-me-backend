from rest_framework import serializers
from .models import UserDetail, User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email']


class UserInfoSerializer(serializers.ModelSerializer):
    user = UserSerializer(many=False)

    class Meta:
        model = UserDetail
        fields = ['user', 'profile_pic', 'first_name',
                  'last_name', 'gender', 'birth_date']
