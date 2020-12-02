from django.shortcuts import render
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status
from .models import User


# Create your views here.

class UserDetailView(GenericAPIView):
    def get(self, request, username):

        if User.objects.filter(username=username).exists():
            user = User.objects.get(username=username)
            user_details = user.details

            data = {
                'user': user.username,
                'email': user.email,
                'first_name': user_details.first_name,
                'last_name': user_details.last_name,
                'profile_pic': '',
                'gender': user_details.gender,
                'birth_date': user_details.birth_date
            }

            if user_details.profile_pic:
                data['profile_pic'] = user_details.profile_pic

            return Response(data, status=status.HTTP_200_OK)

        else:
            return Response({'error': 'Username is invalid.'}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, username):
        if User.objects.filter(username=username).exists():
            user = User.objects.get(username=username).details
            request_data = request.data

            user.first_name = request_data['first_name']
            user.last_name = request_data['last_name']
            user.gender = request_data['gender']
            user.save()

            return Response({'success': 'Profile updated successfully'}, status=status.HTTP_200_OK)

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
            User.objects.get(username=username).delete()

            return Response({'success': 'Your account is now closed, you will no longer have access to your account'}, status=status.HTTP_200_OK)

        else:
            return Response({'error': 'Username is invalid.'}, status=status.HTTP_404_NOT_FOUND)
