from django.shortcuts import render

from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView

from users.models import User
from .models import Workspace, WorkBoard, TaskGroup, Task
from .serializer import WorkspaceSerializer, WorkBoardSerializer, TaskGroupSerializer, TaskSerializer
from .utils import generate_link


# Create your views here.

class WorkspaceListView(GenericAPIView):
    serializer_class = WorkspaceSerializer

    def get(self, request, username):
        if not User.objects.filter(username=username).exists():
            return Response({'error': 'Username is invalid.'}, status=status.HTTP_404_NOT_FOUND)

        user = User.objects.get(username=username)
        workspace_list = [{
            'title': workspace.title,
            'link': workspace.link,
            'leader': workspace.leader.username,
            'members-count': len(workspace.members.all())
        } for workspace in user.workspace.all()]

        return Response({'data': workspace_list}, status=status.HTTP_200_OK)

    # Creating new workspace for user
    def post(self, request, username):
        if not User.objects.filter(username=username).exists():
            return Response({'error': 'Username is invalid.'}, status=status.HTTP_404_NOT_FOUND)

        user = User.objects.get(username=username)
        request.data['leader'] = user.pk
        request.data['link'] = generate_link()

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        data = serializer.data

        return Response({'data': data}, status=status.HTTP_201_CREATED)


class WorkspaceView(GenericAPIView):
    serializer_class = WorkspaceSerializer

    def patch(self, request, username, collab_id):
        if not User.objects.filter(username=username).exists():
            return Response({'error': 'Username is invalid.'}, status=status.HTTP_404_NOT_FOUND)

        user = User.objects.get(username=username)

        if not Workspace.objects.filter(leader=user.pk, id=collab_id):
            return Response({'error': 'Workspace is invalid.'}, status=status.HTTP_404_NOT_FOUND)

        workspace = Workspace.objects.get(leader=user.pk, id=collab_id)

        request.data['leader'] = workspace.leader.pk
        request.data['link'] = workspace.link

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        workspace.title = request.data['title']
        workspace.save()

        return Response({'success': 'Workspace updated successfully.'}, status=status.HTTP_200_OK)

    def delete(self, request, username, collab_id):
        if not User.objects.filter(username=username).exists():
            return Response({'error': 'Username is invalid.'}, status=status.HTTP_404_NOT_FOUND)

        user = User.objects.get(username=username)

        if not Workspace.objects.filter(leader=user.pk, id=collab_id).exists():
            return Response({'error': 'Workspace is invalid.'}, status=status.HTTP_404_NOT_FOUND)

        Workspace.objects.get(leader=user, id=collab_id).delete()

        return Response({'success': 'Workspace deleted successfully.'}, status=status.HTTP_200_OK)


class WorkBoardView(GenericAPIView):
    serializer_class = WorkBoardSerializer

    def get(self, request, username):
        pass

    def post(self, request, username):
        pass


class TaskGroupView(GenericAPIView):
    serializer_class = TaskGroupSerializer

    def get(self, request, username):
        pass

    def post(self, request, username):
        pass


class TaskView(GenericAPIView):
    serializer_class = TaskSerializer

    def get(self, request, username):
        pass

    def post(self, request, username):
        pass
