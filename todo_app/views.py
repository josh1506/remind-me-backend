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
                    'id': todo.id,
                    'title': todo.title,
                    'complete': todo.complete,
                    'date_created': todo.date_created,
                }

                if todo.image:
                    todo_details['image'] = todo.image

                data.append(todo_details)

            return Response({'data': data}, status=status.HTTP_200_OK)

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

        return Response({'success': 'To-do created successfully.'}, status=status.HTTP_201_CREATED)


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
            return Response({'error': 'To-do is invalid'}, status=status.HTTP_404_NOT_FOUND)

        todo = ToDo.objects.get(user=user.pk, id=todo_id)

        todo.title = request.data['title']
        todo.complete = request.data['complete']
        todo.save()

        return Response({'success': 'Updated successfully'}, status=status.HTTP_201_CREATED)

    def delete(self, request, username, todo_id):
        if not User.objects.filter(username=username).exists():
            return Response({'error': 'Username is invalid.'}, status=status.HTTP_404_NOT_FOUND)

        user = User.objects.get(username=username)

        if not ToDo.objects.filter(user=user.pk, id=todo_id).exists():
            return Response({'error': 'To-do not found.'}, status=status.HTTP_404_NOT_FOUND)

        todo = ToDo.objects.get(user=user.pk, id=todo_id)
        todo.delete()

        return Response({'success': 'To-do is now deleted.'}, status=status.HTTP_200_OK)


class ToDoTaskView(GenericAPIView):
    serializer_class = ToDoTaskSerializer

    def get(self, request, username, todo_id):
        if not User.objects.filter(username=username).exists():
            return Response({'error': 'User is invalid.'}, status=status.HTTP_404_NOT_FOUND)

        user = User.objects.get(username=username)

        if not ToDo.objects.filter(id=todo_id, user=user.pk).exists():
            return Response({'error': 'To-do not found.'}, status=status.HTTP_404_NOT_FOUND)

        todo = ToDo.objects.get(id=todo_id, user=user.pk)
        todo_tasks = todo.task.all()
        data = [{
            'todo': task.todo.title,
            'name': task.name,
            'complete': task.complete
        } for task in todo_tasks]

        return Response({'data': data}, status=status.HTTP_200_OK)

    def post(self, request, username, todo_id):
        if not User.objects.filter(username=username).exists():
            return Response({'error': 'User is invalid.'}, status=status.HTTP_404_NOT_FOUND)

        user = User.objects.get(username=username)

        if not ToDo.objects.filter(id=todo_id, user=user.pk).exists():
            return Response({'error': 'To-do not found'}, status=status.HTTP_404_NOT_FOUND)

        todo = ToDo.objects.get(id=todo_id, user=user.pk)

        request.data['todo'] = todo.pk
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        data = serializer.data

        return Response({'success': 'Task created successfully'}, status=status.HTTP_201_CREATED)


class ToDoTaskDetailView(GenericAPIView):
    serializer_class = ToDoTaskSerializer

    def get(self, request, username, todo_id, task_id):
        if not User.objects.filter(username=username).exists():
            return Response({'error': 'User is invalid.'}, status=status.HTTP_404_NOT_FOUND)

        user = User.objects.get(username=username)

        if not ToDo.objects.filter(id=todo_id, user=user.pk).exists():
            return Response({'error': 'To-Do is invalid.'}, status=status.HTTP_404_NOT_FOUND)

        todo = ToDo.objects.get(id=todo_id, user=user.pk)

        if not ToDoTask.objects.filter(id=task_id, todo=todo.pk).exists():
            return Response({'error': 'Invalid task ID'}, status=status.HTTP_404_NOT_FOUND)

        task = ToDoTask.objects.get(id=task_id, todo=todo.pk)

        data = {
            'id': task.id,
            'todo': task.todo.title,
            'name': task.name,
            'complete': task.complete,
        }

        return Response({'data': data}, status=status.HTTP_200_OK)

    def put(self, request, username, todo_id, task_id):
        if not User.objects.filter(username=username).exists():
            return Response({'error': 'User is invalid.'}, status=status.HTTP_404_NOT_FOUND)

        user = User.objects.get(username=username)

        if not ToDo.objects.filter(id=todo_id, user=user.pk).exists():
            return Response({'error': 'To-Do is invalid.'}, status=status.HTTP_404_NOT_FOUND)

        todo = ToDo.objects.get(id=todo_id, user=user.pk)

        if not ToDoTask.objects.filter(id=task_id, todo=todo.pk).exists():
            return Response({'error': 'Invalid task ID'}, status=status.HTTP_404_NOT_FOUND)

        task = ToDoTask.objects.get(id=task_id, todo=todo.pk)

        request.data['todo'] = todo_task.todo.pk
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer_data = serializer.data

        todo_task.name = serializer_data['name']
        todo_task.complete = serializer_data['complete']
        todo_task.save()

        return Response({'success': 'Task updated successfully'}, status=status.HTTP_200_OK)

    def delete(self, request, username, todo_id, task_id):
        if not User.objects.filter(username=username).exists():
            return Response({'error': 'User is invalid.'}, status=status.HTTP_404_NOT_FOUND)

        user = User.objects.get(username=username)

        if not ToDo.objects.filter(id=todo_id, user=user.pk).exists():
            return Response({'error': 'To-Do is invalid.'}, status=status.HTTP_404_NOT_FOUND)

        todo = ToDo.objects.get(id=todo_id, user=user.pk)

        if not ToDoTask.objects.filter(id=task_id, todo=todo.pk).exists():
            return Response({'error': 'Task ID not found.'}, status=status.HTTP_404_NOT_FOUND)

        ToDoTask.objects.get(id=task_id, todo=todo.pk).delete()

        return Response({'success': 'Task is deleted successfully'}, status=status.HTTP_200_OK)
