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


class ToDoListDetailView(GenericAPIView):
    serializer_class = ToDoSerializer

    def get(self, request, username, todo_id):
        if not User.objects.filter(username=username):
            return Response({'error': 'Username is invalid.'}, status=status.HTTP_404_NOT_FOUND)

        user = User.objects.get(username=username)

        if not ToDo.objects.filter(id=todo_id, user=user).exists():
            return Response({'error': 'To-do details not found.'}, status=status.HTTP_404_NOT_FOUND)

        todo = ToDo.objects.get(id=todo_id, user=user)
        task_list = todo.task.all()

        data = {
            'id': todo.id,
            'user': todo.user.username,
            'title': todo.title,
            'tasks': [{
                'id': task.id,
                'name': task.name,
                'complete': task.complete,
            } for task in task_list],
            'complete': todo.complete
        }

        if todo.image:
            data['image'] = todo.image

        return Response({'data': data}, status=status.HTTP_200_OK)

    def put(self, request, username, todo_id):
        if not User.objects.filter(username=username).exists():
            return Response({'error': 'Username is invalid.'}, status=status.HTTP_404_NOT_FOUND)

        user = User.objects.get(username=username)

        if not ToDo.objects.filter(user=user.pk, id=todo_id).exists():
            return Response({'error': 'Todo is invalid'}, status=status.HTTP_404_NOT_FOUND)

        todo = ToDo.objects.get(user=user.pk, id=todo_id)

        todo.title = request.data['title']
        todo.save()

        return Response({'success': 'Updated successfully'}, status=status.HTTP_201_CREATED)

    def delete(self, request, username, todo_id):
        if not User.objects.filter(username=username).exists():
            return Response({'error': 'Username is invalid.'}, status=status.HTTP_404_NOT_FOUND)

        user = User.objects.get(username=username)

        if not ToDo.objects.filter(user=user.pk, id=todo_id).exists():
            return Response({'error': 'Todo not found.'}, status=status.HTTP_404_NOT_FOUND)

        todo = ToDo.objects.get(user=user.pk, id=todo_id)
        todo.delete()

        return Response({'success': 'Todo is now deleted.'}, status=status.HTTP_200_OK)
