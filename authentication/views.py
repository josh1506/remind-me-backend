import jwt

from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.sites.shortcuts import get_current_site
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render
from django.conf import settings
from django.urls import reverse
from django.utils.encoding import (
    smart_bytes, smart_str, force_str, DjangoUnicodeDecodeError)

from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status

from .serializer import UserRegisterSerializer, UserLoginSerializer, UserRequestPasswordResetSerializer
from .renderer import UserRegisterRenderer
from .models import User
from .utility import Utils


# Create your views here.
class UserRegisterView(GenericAPIView):
    serializer_class = UserRegisterSerializer
    renderer_classes = (UserRegisterRenderer, )

    def post(self, request):
        data = request.data
        serializer = self.serializer_class(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        user_data = serializer.data

        user = User.objects.get(email=user_data['email'])
        token = str(RefreshToken.for_user(user).access_token)

        current_site = get_current_site(request)
        link = reverse('verify-email', kwargs={'token': token})
        url = f'http://{current_site.domain}{link}'

        email_subject = 'Email Verification'
        email_body = f'Hello {user.username}, \n \n Thank you for registering to RemindMe! \n \n In order for your Account to be active, we need to verify your email address. Please use the verification URL below to confirm your email address and complete the application process. \n \n {url} \n \n Thank you,'
        email_to = user.email

        email = {'subject': email_subject, 'body': email_body, 'to': email_to}
        Utils.send_email(email)

        message = "Account created successfully. Please check your email's inbox or spam folder to verify your account."

        return Response({'user_data': data, 'message': message}, status=status.HTTP_201_CREATED)


class UserEmailVerificationView(GenericAPIView):
    def get(self, request, token):
        try:
            data = jwt.decode(token, settings.SECRET_KEY)
            user = User.objects.get(id=data.get('user_id'))

            if not user.is_verified:
                user.is_verified = True
                user.save()

            return Response({'success': 'Account is now activated'}, status=status.HTTP_200_OK)

        except jwt.ExpiredSignature:
            return Response({'error': 'Token is already expired. Please request another one.'}, status=status.HTTP_400_BAD_REQUEST)

        except jwt.DecodeError:
            return Response({'error': 'Token is invalid'}, status=status.HTTP_404_NOT_FOUND)


class UserLoginView(GenericAPIView):
    serializer_class = UserLoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class UserRequestPasswordResetView(GenericAPIView):
    serializer_class = UserRequestPasswordResetSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user_data = serializer.data

        try:
            user = User.objects.get(email=user_data['email'])
            uidb64 = urlsafe_base64_encode(smart_bytes(user.id))
            token = PasswordResetTokenGenerator().make_token(user)

            current_site = get_current_site(request)
            link = reverse('validate-password-reset',
                           kwargs={'uidb64': uidb64, 'token': token})
            url = f'http://{current_site}{link}'

            email_subject = 'Password Reset'
            email_body = f'Hello {user.username}, \n \nPlease click the link below to reset your password \n \n{url} \n \nThank you,'
            email_to = user.email

            email = {'subject': email_subject,
                     'body': email_body, 'to': email_to}
            Utils.send_email(email)

            return Response({'success': "We have sent you an email for reseting your password. Please check in your email's inbox or spam folder."}, status=status.HTTP_200_OK)

        except ObjectDoesNotExist:
            return Response({'error': 'Invalid email address.'}, status=status.HTTP_404_NOT_FOUND)

        except:
            return Response({'error': 'There was an error. Please try again'}, status=status.HTTP_400_BAD_REQUEST)


class VerifyPasswordResetTokenView(GenericAPIView):
    def get(self, request, uidb64, token):
        try:
            id = urlsafe_base64_decode(uidb64)
            user = User.objects.get(id=id)

            if not PasswordResetTokenGenerator().check_token(user, token):
                return Response({'error': 'Token is already used. Please try another one'}, status=status.HTTP_401_UNAUTHORIZED)

            return Response({'success': 'Credentials is valid', 'uidb64': uidb64, 'token': token}, status=status.HTTP_200_OK)

        except DjangoUnicodeDecodeError:
            return Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)
