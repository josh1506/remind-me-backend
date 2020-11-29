import random
import string
import environ
from users.models import User
from django.contrib.auth import authenticate
from rest_framework.exceptions import AuthenticationFailed

env = environ.Env(DEBUG=(bool, False))
environ.Env.read_env('../.env')


def generate_username(name):
    username = ''.join(name.split(' ').lower())

    if not User.objects.filter(username=username):
        return username

    else:
        letters_and_numbers = string.ascii_letters + string.digits
        unique_string = ''.join(random.choice(
            letters_and_numbers) for i in range(5))
        unique_username = username + unique_string

        return generate_username(unique_username)


def user_social_register(user_id, email, name, provider):
    check_user = User.objects.filter(email=email)

    if check_user.exists():
        if check_user[0].auth_provider == provider:
            registered_user = authenticate(
                email=email, password=env('SECRET_KEY'))

            data = {
                'username': registered_user.username,
                'email': registered_user.email,
                'tokens': registered_user.get_token(),
            }

        else:
            return {
                'error': f'Please continue your login using {check_user[0].auth_provider}'}

    else:
        user_info = {
            'username': generate_username(name),
            'email': email,
            'password': env('SECRET_KEY')
        }

        user = User.objects.create_user(**user_info)
        user.is_verified = True
        user.is_active = True
        user.auth_provider = provider
        user.save()

        user_auth = authenticate(email=email, password=env('SECRET_KEY'))

        data = {
            'username': user_auth.username,
            'email': user_auth.email,
            'tokens': user_auth.get_token()}

        return data
