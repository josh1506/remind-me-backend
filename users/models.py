from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from rest_framework_simplejwt.tokens import RefreshToken


# Create your models here.

class UserManager(BaseUserManager):
    def create_user(self, username, email, password=None):
        if username is None:
            raise TypeError('Username is required')

        if email is None:
            raise TypeError('Email is required')

        user = self.model(username=username, email=email)
        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, username, email, password):
        if password is None:
            raise TypeError('Password is required')

        user = self.create_user(username, email, password)
        user.is_superuser = True
        user.is_staff = True
        user.save()

        return user


class User(AbstractBaseUser, PermissionsMixin):
    AUTHENTICATION_PROVIDER = [('email', 'email'), ('facebook', 'facebook')]

    username = models.CharField(max_length=255, db_index=True, unique=True)
    email = models.EmailField(
        max_length=255, blank=False, db_index=True, unique=True)
    auth_provider = models.CharField(
        max_length=255, choices=AUTHENTICATION_PROVIDER, default='email')
    is_verified = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    joined_date = models.DateTimeField(auto_now=True)

    REQUIRED_FIELDS = ['username']
    USERNAME_FIELD = 'email'

    objects = UserManager()

    def __str__(self):
        return self.email

    def get_token(self):
        refresh_token = RefreshToken.for_user(self)
        access_token = refresh_token.access_token

        tokens = {
            'refresh-token': str(refresh_token),
            'access-token': str(access_token)
        }

        return tokens


class UserDetail(models.Model):
    GENDER = [('male', 'Male'), ('female', 'Female')]

    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='details')
    profile_pic = models.ImageField(blank=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    gender = models.CharField(max_length=15, choices=GENDER)
    birth_date = models.DateField(blank=True)

    def __str__(self):
        return self.user.username
