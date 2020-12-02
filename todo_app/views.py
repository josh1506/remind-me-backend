from django.shortcuts import render

from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from rest_framework import viewsets
from rest_framework import status

from users.models import User
from .models import ToDo, ToDoTask
from .serializer import ToDoSerializer, ToDoTaskSerializer


# Create your views here.

class ToDoListView(GenericAPIView):
    serializer_class = ToDoSerializer

    def get(self, request, username):
        if User.objects.filter(username=username).exists():
            user = User.objects.get(username=username)
            todo_list = ToDo.objects.filter(user=user.pk)
            data = []
            for todo in todo_list:
                todo_details = {
                    'title': todo.title,
                    'complete': todo.complete,
                    'date_created': todo.date_created,
                }

                if todo.image:
                    todo_details['image'] = todo.image

                data.append(todo_details)

            return Response({'success': {'data': data}}, status=status.HTTP_200_OK)

        else:
            return Response({'error': 'Username is invalid.'}, status=status.HTTP_404_NOT_FOUND)

    def post(self, request, username):
        if not User.objects.filter(username=username).exists():
            return Response({'error': 'Username is invalid'})

        user = User.objects.get(username=username)
        request.data['user'] = user.pk
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        data = serializer.data

        return Response(data)
