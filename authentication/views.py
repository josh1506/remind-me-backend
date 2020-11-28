from django.shortcuts import render
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse

from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status

from .serializer import UserRegisterSerializer
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
        url = f'https://{current_site.domain}{link}'

        email_subject = 'Email Verification'
        email_body = f'Hello {user.username}, \n \n Thank you for registering to RemindMe! \n \n In order for your Account to be active, we need to verify your email address. Please use the verification URL below to confirm your email address and complete the application process. \n \n {url} \n \n Thank you,'
        email_to = user.email

        email = {'subject': email_subject, 'body': email_body, 'to': email_to}
        Utils.send_email(email)

        message = "Account created successfully. Please check your email's inbox or spam folder to verify your account."

        return Response({'user_data': data, 'message': message}, status=status.HTTP_201_CREATED)


class UserEmailVerificationView(GenericAPIView):
    def get(self, request, token):
        pass
