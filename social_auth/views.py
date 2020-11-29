from django.shortcuts import render

from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status

from .serializer import FacebookSocialAuthSerializer


# Create your views here.

class FacebookSocialAuthView(GenericAPIView):
    serializer_class = FacebookSocialAuthSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        auth_token = str(request.data['auth_token'])
        data = serializer.validate_auth_token(auth_token)

        return Response({'data': data}, status=status.HTTP_200_OK)
