from django.shortcuts import render
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status
from .serializer import UserInfoSerializer
from .models import User


# Create your views here.

class UserDetailView(GenericAPIView):
    serializer_class = UserInfoSerializer

    def get(self, request, username):
        serializer = self.serializer_class(data=request.data)

        if User.objects.filter(username=username).exists():
            user = User.objects.get(username=username)
            user_details = user.details

            data = {
                'user': user.username,
                'email': user.email,
                'first_name': user_details.first_name,
                'last_name': user_details.last_name,
                'gender': user_details.gender,
                'birth_date': user_details.birth_date
            }

            return Response(data, status=status.HTTP_200_OK)

        else:
            return Response({'error': 'Username is invalid.'}, status=status.HTTP_404_NOT_FOUND)

    def post(self, request, username):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid()
        request_data = serializer.data

        if User.objects.filter(username=username).exists():
            user = User.objects.get(username=username)
            user_details = user.details

            user_details.first_name = request_data['first_name']
            user_details.last_name = request_data['last_name']
            user_details.gender = request_data['gender']
            user_details.birth_date = request_data['birth_date']
            user_details.save()

            data = {
                'user': user.username,
                'email': user.email,
                'first_name': user_details.first_name,
                'last_name': user_details.last_name,
                'gender': user_details.gender,
                'birth_date': user_details.birth_date
            }

            return Response({'data': data}, status=status.HTTP_200_OK)

        else:
            return Response({'error': 'Username is invalid.'}, status=status.HTTP_404_NOT_FOUND)


class UserDisableAccountView(GenericAPIView):
    def patch(self, request, username):
        if User.objects.filter(username=username).exists():
            user = User.objects.get(username=username)

            if not user.is_verified:
                return Response({'error': 'Email is not verified. Please check your email inbox or spam folder to verify account.'}, status=status.HTTP_400_BAD_REQUEST)

            if user.is_active:
                user.is_active = False
                user.save()

            return Response({'success': 'Your account is now disabled.'}, status=status.HTTP_200_OK)

        else:
            return Response({'error': 'Username is invalid.'}, status=status.HTTP_404_NOT_FOUND)


class UserRecoverAccountView(GenericAPIView):
    def patch(self, request, username):
        if User.objects.filter(username=username).exists():
            user = User.objects.get(username=username)

            if not user.is_verified:
                return Response({'error': 'Email is not verified. Please check your email inbox or spam folder to verify account.'}, status=status.HTTP_400_BAD_REQUEST)

            if not user.is_active:
                user.is_active = True
                user.save()

            return Response({'success': 'Your account is now activated.'}, status=status.HTTP_200_OK)

        else:
            return Response({'error': 'Username is invalid.'}, status=status.HTTP_404_NOT_FOUND)


class UserDeleteAccountView(GenericAPIView):
    def delete(self, request, username):
        if User.objects.filter(username=username).exists():
            user = User.objects.get(username=username)
            user.delete()

            return Response({'success': 'Your account is now closed, you will no longer have access to your account'}, status=status.HTTP_200_OK)

        else:
            return Response({'error': 'Username is invalid.'}, status=status.HTTP_404_NOT_FOUND)
