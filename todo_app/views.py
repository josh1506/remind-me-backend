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
            todo_list_data = ToDo.objects.filter(user=user)
            todo_list = []

            for todo in todo_list_data:
                data = {
                    'user': todo.user.username,
                    'title': todo.title,
                    'complete': todo.complete,
                    'date_created': todo.date_created
                }

                if todo.image:
                    data['image'] = todo.image

                todo_list.append(data)

            return Response({'success': {'data': todo_list}}, status=status.HTTP_200_OK)

        else:
            return Response({'error': 'Username is invalid.'}, status=status.HTTP_404_NOT_FOUND)


class ToDoListDetailView(GenericAPIView):
    def get(self, request, username, todo_id):
        pass
