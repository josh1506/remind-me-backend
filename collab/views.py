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
            'members-count': workspace.members_count()
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

    def patch(self, request, username, workspace_id):
        if not User.objects.filter(username=username).exists():
            return Response({'error': 'Username is invalid.'}, status=status.HTTP_404_NOT_FOUND)

        user = User.objects.get(username=username)

        if not Workspace.objects.filter(leader=user.pk, id=workspace_id):
            return Response({'error': 'Workspace is invalid.'}, status=status.HTTP_404_NOT_FOUND)

        workspace = Workspace.objects.get(leader=user.pk, id=workspace_id)

        request.data['leader'] = workspace.leader.pk
        request.data['link'] = workspace.link

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        workspace.title = request.data['title']
        workspace.save()

        return Response({'success': 'Workspace updated successfully.'}, status=status.HTTP_200_OK)

    def delete(self, request, username, workspace_id):
        if not User.objects.filter(username=username).exists():
            return Response({'error': 'Username is invalid.'}, status=status.HTTP_404_NOT_FOUND)

        user = User.objects.get(username=username)

        if not Workspace.objects.filter(leader=user.pk, id=workspace_id).exists():
            return Response({'error': 'Workspace is invalid.'}, status=status.HTTP_404_NOT_FOUND)

        Workspace.objects.get(leader=user, id=workspace_id).delete()

        return Response({'success': 'Workspace deleted successfully.'}, status=status.HTTP_200_OK)


class WorkBoardListView(GenericAPIView):
    serializer_class = WorkBoardSerializer

    def get(self, request, username, workspace_id):
        if not User.objects.filter(username=username).exists():
            return Response({'error': 'Username is invalid.'}, status=status.HTTP_404_NOT_FOUND)

        user = User.objects.get(username=username)

        if not Workspace.objects.filter(id=workspace_id).exists():
            return Response({'error': 'Workspace is invalid'}, status=status.HTTP_404_NOT_FOUND)

        workspace_leader = Workspace.objects.get(
            id=workspace_id).leader.username

        workboard = []

        if username == workspace_leader:
            workboard = [{
                'id': workboard.pk,
                'title': workboard.title,
                'privacy': workboard.privacy,
                'members-count': workboard.members_count()
            } for workboard in WorkBoard.objects.filter(
                workspace=workspace_id)]

        else:
            workboard = [{
                'id': workboard.pk,
                'title': workboard.title,
                'privacy': workboard.privacy,
                'members-count': workboard.members_count()
            } for workboard in WorkBoard.objects.filter(
                workspace=workspace_id, privacy='public', members=user.pk)]

        return Response({'data': workboard}, status=status.HTTP_200_OK)

    def post(self, request, username, workspace_id):
        if not User.objects.filter(username=username).exists():
            return Response({'error': 'Username is invalid.'}, status=status.HTTP_404_NOT_FOUND)

        user = User.objects.get(username=username)

        if not Workspace.objects.filter(id=workspace_id).exists():
            return Response({'error': 'Workspace is invalid'}, status=status.HTTP_404_NOT_FOUND)

        workspace_leader = Workspace.objects.get(
            id=workspace_id).leader.username

        if username == workspace_leader:
            request.data['workspace'] = workspace_id

            serializer = self.serializer_class(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()

            data = serializer.data

            return Response({'data': data}, status=status.HTTP_201_CREATED)

        else:
            return Response({'error': 'User is not authorize for this kind of action.'}, status=status.HTTP_401_UNAUTHORIZED)


class WorkBoardDetailView(GenericAPIView):
    serializer_class = WorkBoardSerializer

    def put(self, request, username, workspace_id, workboard_id):
        if not User.objects.filter(username=username).exists():
            return Response({'error': 'User is invalid.'}, status=status.HTTP_404_NOT_FOUND)

        user = User.objects.get(username=username)

        if not Workspace.objects.filter(members=user.pk, id=workspace_id):
            return Response({'error': 'Worksapce is invalid.'}, status=status.HTTP_404_NOT_FOUND)

        worksapce = Workspace.objects.get(id=workspace_id, members=user.pk)

        if not WorkBoard.objects.filter(id=workboard_id, workspace=worksapce.pk, members=user.pk).exists():
            return Response({'error': 'WorkBoard is invalid.'}, status=status.HTTP_404_NOT_FOUND)

        if worksapce.leader.username == user.username:
            request.data['workspace'] = worksapce.pk
            serializer = self.serializer_class(data=request.data)
            serializer.is_valid(raise_exception=True)

            workboard = WorkBoard.objects.get(
                id=workboard_id, workspace=worksapce.pk, members=user.pk)
            workboard.title = request.data['title']
            workboard.privacy = request.data['privacy']
            workboard.save()

            return Response({'success': 'WorkBoard updated successfully.'}, status=status.HTTP_200_OK)

        else:
            return Response({'error': 'User is not authorize for this kind of action.'}, status=status.HTTP_401_UNAUTHORIZED)

    def delete(self, request, username, workspace_id, workboard_id):
        if not User.objects.filter(username=username).exists():
            return Response({'error': 'User is invalid.'}, status=status.HTTP_404_NOT_FOUND)

        user = User.objects.get(username=username)

        if not Workspace.objects.filter(members=user.pk, id=workspace_id):
            return Response({'error': 'Worksapce is invalid.'}, status=status.HTTP_404_NOT_FOUND)

        worksapce = Workspace.objects.get(id=workspace_id, members=user.pk)

        if not WorkBoard.objects.filter(id=workboard_id, workspace=worksapce.pk, members=user.pk).exists():
            return Response({'error': 'WorkBoard is invalid.'}, status=status.HTTP_404_NOT_FOUND)

        if worksapce.leader.username == user.username:
            WorkBoard.objects.get(
                id=workboard_id, workspace=worksapce.pk, members=user.pk).delete()

            return Response({'success': 'Workboard deleted successfully.'}, status=status.HTTP_200_OK)

        else:
            return Response({'error': 'User is not authorize for this kind of action.'}, status=status.HTTP_401_UNAUTHORIZED)


class TaskGroupListView(GenericAPIView):
    serializer_class = TaskGroupSerializer

    def get(self, request, username, workspace_id, workboard_id):
        if not User.objects.filter(username=username).exists():
            return Response({'error': 'User is invalid.'}, status=status.HTTP_404_NOT_FOUND)

        user = User.objects.get(username=username)

        if not Workspace.objects.filter(id=workspace_id, members=user.pk):
            return Response({'error': 'Workspace is invalid.'}, status=status.HTTP_404_NOT_FOUND)

        workspace = Workspace.objects.get(id=workspace_id, members=user.pk)

        if not WorkBoard.objects.filter(id=workboard_id, workspace=workspace.pk, members=user.pk):
            return Response({'error': 'WorkBoard is invalid.'}, status=status.HTTP_404_NOT_FOUND)

        workboard = WorkBoard.objects.get(
            id=workboard_id, workspace=workspace.pk, members=user.pk)
        task_group = [{
            'id': task_group.pk,
            'title': task_group.title,
            'progress': task_group.progress()
        } for task_group in workboard.task_group.all()]

        return Response({'data': task_group}, status=status.HTTP_200_OK)

    def post(self, request, username, workspace_id, workboard_id):
        if not User.objects.filter(username=username).exists():
            return Response({'error': 'User is invalid.'}, status=status.HTTP_404_NOT_FOUND)

        user = User.objects.get(username=username)

        if not Workspace.objects.filter(id=workspace_id, members=user.pk):
            return Response({'error': 'Workspace is invalid.'}, status=status.HTTP_404_NOT_FOUND)

        workspace = Workspace.objects.get(id=workspace_id, members=user.pk)

        if not WorkBoard.objects.filter(id=workboard_id, workspace=workspace.pk, members=user.pk):
            return Response({'error': 'WorkBoard is invalid.'}, status=status.HTTP_404_NOT_FOUND)

        workboard = WorkBoard.objects.get(
            id=workboard_id, workspace=workspace.pk, members=user.pk)

        if workspace.leader.username == user.username:
            request.data['work_board'] = workboard.pk

            serializer = self.serializer_class(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()

            data = serializer.data

            return Response({'data': data}, status=status.HTTP_201_CREATED)

        else:
            return Response({'error': 'User is not authorize for this kind of action.'}, status=status.HTTP_401_UNAUTHORIZED)


class TaskGroupDetailView(GenericAPIView):
    serializer_class = TaskGroupSerializer

    def put(self, request, username, workspace_id, workboard_id, taskgroup_id):
        if not User.objects.filter(username=username).exists():
            return Response({'error': 'User is invalid.'}, status=status.HTTP_404_NOT_FOUND)

        user = User.objects.get(username=username)

        if not Workspace.objects.filter(id=workspace_id, members=user.pk).exists():
            return Response({'error': 'Workspace is invalid.'}, status=status.HTTP_404_NOT_FOUND)

        worksapce = Workspace.objects.get(id=workspace_id, members=user.pk)

        if not WorkBoard.objects.filter(id=workboard_id, workspace=worksapce.pk, members=user.pk):
            return Response({'error': 'WorkBoard is invalid.'}, status=status.HTTP_404_NOT_FOUND)

        workboard = WorkBoard.objects.get(
            id=workboard_id, workspace=worksapce.pk)

        if not TaskGroup.objects.filter(id=taskgroup_id, work_board=workboard.pk).exists():
            return Response({'error': 'TaskGroup is invalid.'}, status=status.HTTP_404_NOT_FOUND)

        if worksapce.leader.username == user.username:
            request.data['work_board'] = workboard.pk
            serializer = self.serializer_class(data=request.data)
            serializer.is_valid()

            task_group = TaskGroup.objects.get(
                id=taskgroup_id, work_board=workboard.pk)
            task_group.title = request.data['title']
            task_group.save()

            return Response({'success': 'TaskGroup updated successfully.'}, status=status.HTTP_200_OK)

        else:
            return Response({'error': 'User is not authorize for this kind of action.'}, status=status.HTTP_401_UNAUTHORIZED)

    def delete(self, request, username, workspace_id, workboard_id, taskgroup_id):
        if not User.objects.filter(username=username).exists():
            return Response({'error': 'User is invalid.'}, status=status.HTTP_404_NOT_FOUND)

        user = User.objects.get(username=username)

        if not Workspace.objects.filter(id=workspace_id, members=user.pk).exists():
            return Response({'error': 'Workspace is invalid.'}, status=status.HTTP_404_NOT_FOUND)

        worksapce = Workspace.objects.get(id=workspace_id, members=user.pk)

        if not WorkBoard.objects.filter(id=workboard_id, workspace=worksapce.pk, members=user.pk):
            return Response({'error': 'WorkBoard is invalid.'}, status=status.HTTP_404_NOT_FOUND)

        workboard = WorkBoard.objects.get(
            id=workboard_id, workspace=worksapce.pk)

        if not TaskGroup.objects.filter(id=taskgroup_id, work_board=workboard.pk).exists():
            return Response({'error': 'TaskGroup is invalid.'}, status=status.HTTP_404_NOT_FOUND)

        if worksapce.leader.username == user.username:
            TaskGroup.objects.get(
                id=taskgroup_id, work_board=workboard.pk).delete()

            return Response({'success': 'WorkBoard deleted successfully.'}, status=status.HTTP_200_OK)

        else:
            return Response({'error': 'User is not authorize for this kind of action.'}, status=status.HTTP_401_UNAUTHORIZED)


class TaskView(GenericAPIView):
    serializer_class = TaskSerializer

    def get(self, request, username):
        pass

    def post(self, request, username):
        pass
