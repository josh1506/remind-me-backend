from django.shortcuts import render

from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView

from users.models import User
from .utils import generate_link
from .custom_middleware import Custom_Middleware as middleware
from .models import (Workspace, WorkBoard, TaskGroup, Task, TaskComment)
from .serializer import (WorkspaceSerializer, WorkBoardSerializer,
                         TaskGroupSerializer, TaskSerializer,
                         TaskCommentSerializer)


# Create your views here.

class WorkspaceListView(GenericAPIView):
    serializer_class = WorkspaceSerializer

    # Getting all list of user workspace
    def get(self, request, username):
        serializer = self.serializer_class()
        workspace = serializer.get_workspace_list(username)

        return Response({'data': workspace}, status=status.HTTP_200_OK)

    # Creating new workspace for user
    def post(self, request, username):
        user = middleware.validate_user(username)
        request.data['leader'] = user.pk
        request.data['link'] = generate_link()

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        data = serializer.data

        return Response({'data': data}, status=status.HTTP_201_CREATED)


class WorkspaceDetailView(GenericAPIView):
    serializer_class = WorkspaceSerializer

    def patch(self, request, username, workspace_id):
        user = middleware.validate_user(username=username)
        workspace = middleware.validate_workspace(
            user=user, workspace_id=workspace_id)

        # Only leader is authorized to update the workspace
        middleware.is_leader(user, workspace)

        request.data['leader'] = workspace.leader.pk
        request.data['link'] = workspace.link

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.update_workspace(workspace, serializer.data)

        return Response({'success': 'Workspace updated successfully.'}, status=status.HTTP_200_OK)

    def delete(self, request, username, workspace_id):
        user = middleware.validate_user(username=username)
        workspace = middleware.validate_workspace(
            user=user, workspace_id=workspace_id)

        # Only leader is authorized to delete the workspace
        middleware.is_leader(user, workspace)
        workspace.delete()

        return Response({'success': 'Workspace deleted successfully.'}, status=status.HTTP_200_OK)


class WorkBoardListView(GenericAPIView):
    serializer_class = WorkBoardSerializer

    def get(self, request, username, workspace_id):
        serializer = self.serializer_class()
        user = middleware.validate_user(username)
        workspace = middleware.validate_workspace(
            user=user, workspace_id=workspace_id)

        # If user is not the leader then they can only see the workboard that they're in
        workboard = serializer.get_workboard_list(user, workspace)

        return Response({'data': workboard}, status=status.HTTP_200_OK)

    def post(self, request, username, workspace_id):
        user = middleware.validate_user(username)
        workspace = middleware.validate_workspace(
            user=user, workspace_id=workspace_id)

        request.data['user'] = user
        request.data['workspace-leader'] = workspace.leader.username
        request.data['workspace'] = workspace.pk

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        workboard = serializer.data

        return Response({'data': workboard}, status=status.HTTP_201_CREATED)


class WorkBoardDetailView(GenericAPIView):
    serializer_class = WorkBoardSerializer

    def put(self, request, username, workspace_id, workboard_id):
        user = middleware.validate_user(username=username)
        workspace = middleware.validate_workspace(
            user=user, workspace_id=workspace_id)

        workboard = middleware.validate_workboard(
            user=user, workspace=workspace, workboard_id=workboard_id)

        # Only leader is authorized to update workboard details inside their workspace
        middleware.is_leader(user, workspace)

        request.data['workspace'] = workspace.pk
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.update_workboard(
            workboard=workboard, data=serializer.data)

        return Response({'success': 'WorkBoard updated successfully.'}, status=status.HTTP_200_OK)

    def delete(self, request, username, workspace_id, workboard_id):
        user = middleware.validate_user(username=username)
        workspace = middleware.validate_workspace(
            user=user, workspace_id=workspace_id)
        workboard = middleware.validate_workboard(
            user=user, workspace=workspace, workboard_id=workboard_id)

        # Only leader is authorized to delete workboard inside their workspace
        middleware.is_leader(user, workspace)
        workboard.delete()

        return Response({'success': 'Workboard deleted successfully.'}, status=status.HTTP_200_OK)


class TaskGroupListView(GenericAPIView):
    serializer_class = TaskGroupSerializer

    def get(self, request, username, workspace_id, workboard_id):
        serializer = self.serializer_class()
        user = middleware.validate_user(username=username)
        workspace = middleware.validate_workspace(
            user=user, workspace_id=workspace_id)
        workboard = middleware.validate_workboard(
            user=user, workspace=workspace, workboard_id=workboard_id)

        task_group = serializer.get_taskgroup_list(workboard)

        return Response({'data': task_group}, status=status.HTTP_200_OK)

    def post(self, request, username, workspace_id, workboard_id):
        user = middleware.validate_user(username=username)
        workspace = middleware.validate_workspace(
            user=user, workspace_id=workspace_id)
        workboard = middleware.validate_workboard(
            user=user, workspace=workspace, workboard_id=workboard_id)

        # Only leader is authorized to create task group inside workboard
        middleware.is_leader(user, workspace)

        request.data['work_board'] = workboard.pk
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        data = serializer.data

        return Response({'data': data}, status=status.HTTP_201_CREATED)


class TaskGroupDetailView(GenericAPIView):
    serializer_class = TaskGroupSerializer

    def put(self, request, username, workspace_id, workboard_id, taskgroup_id):
        user = middleware.validate_user(username=username)
        workspace = middleware.validate_workspace(
            user=user, workspace_id=workspace_id)
        workboard = middleware.validate_workboard(
            user=user, workspace=workspace, workboard_id=workboard_id)
        task_group = middleware.validate_task_group(
            workboard=workboard, taskgroup_id=taskgroup_id)

        # Only leader is authorized to update task group inside workboard
        middleware.is_leader(user=user, workspace=workspace)

        request.data['work_board'] = workboard.pk
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid()

        task_group.title = serializer.data['title']
        task_group.save()

        return Response({'success': 'TaskGroup updated successfully.'}, status=status.HTTP_200_OK)

    def delete(self, request, username, workspace_id, workboard_id, taskgroup_id):
        user = middleware.validate_user(username=username)
        workspace = middleware.validate_workspace(
            user=user, workspace_id=workspace_id)
        workboard = middleware.validate_workboard(
            user=user, workspace=workspace, workboard_id=workboard_id)
        task_group = middleware.validate_task_group(
            workboard=workboard, taskgroup_id=taskgroup_id)

        # Only leader is authorized to delete task group inside workboard
        middleware.is_leader(user=user, workspace=workspace)
        task_group.delete()

        return Response({'success': 'WorkBoard deleted successfully.'}, status=status.HTTP_200_OK)


class TaskListView(GenericAPIView):
    serializer_class = TaskSerializer

    def get(self, request, username, workspace_id, workboard_id, taskgroup_id):
        user = middleware.validate_user(username)
        workspace = middleware.validate_workspace(
            user=user, workspace_id=workspace_id)
        workboard = middleware.validate_workboard(
            user=user, workspace=workspace, workboard_id=workboard_id)
        task_group = middleware.validate_task_group(
            workboard=workboard, taskgroup_id=taskgroup_id)

        serializer = self.serializer_class()
        task = serializer.get_task_list(task_group)

        return Response({'data': task}, status=status.HTTP_200_OK)

    def post(self, request, username, workspace_id, workboard_id, taskgroup_id):
        user = User.objects.get(username=username)
        workspace = Workspace.objects.get(id=workspace_id, members=user.pk)
        workboard = WorkBoard.objects.get(
            id=workboard_id, workspace=workspace.pk, members=user.pk)
        task_group = TaskGroup.objects.get(
            id=taskgroup_id, work_board=workboard.pk)

        # Only leader is authorized to create task
        middleware.is_leader(user=user, workspace=workspace)

        request.data['task_group'] = task_group.pk
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        task = serializer.data

        return Response({'data': task}, status=status.HTTP_201_CREATED)


class TaskDetailView(GenericAPIView):
    serializer_class = TaskSerializer

    def put(self, request, username, workspace_id, workboard_id, taskgroup_id, task_id):
        user = User.objects.get(username=username)
        workspace = Workspace.objects.get(id=workspace_id, members=user.pk)
        workboard = WorkBoard.objects.get(
            id=workboard_id, workspace=workspace.pk, members=user.pk)
        task_group = TaskGroup.objects.get(
            id=taskgroup_id, work_board=workboard.pk)
        task = middleware.validate_task(task_id=task_id, taskgroup=task_group)

        # Only leader is authorized to update task
        middleware.is_leader(user=user, workspace=workspace)

        request.data['task_group'] = task_group.pk
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        task_detail = serializer.data

        task.task = task_detail['task']
        task.status = task_detail['status']
        task.due_date = task_detail['due_date']
        task.save()

        return Response({'success': 'Task updated successfully.'}, status=status.HTTP_200_OK)

    def delete(self, request, username, workspace_id, workboard_id, taskgroup_id, task_id):
        user = User.objects.get(username=username)
        workspace = Workspace.objects.get(id=workspace_id, members=user.pk)
        workboard = WorkBoard.objects.get(
            id=workboard_id, workspace=workspace.pk, members=user.pk)
        task_group = TaskGroup.objects.get(
            id=taskgroup_id, work_board=workboard.pk)
        task = middleware.validate_task(task_id=task_id, taskgroup=task_group)

        # Only leader is authorized to delete task
        middleware.is_leader(user=user, workspace=workspace)
        Task.objects.get(id=task_id, task_group=task_group.pk).delete()

        return Response({'success': 'Task deleted successfully.'}, status=status.HTTP_200_OK)


class TaskCommentListView(GenericAPIView):
    serializer_class = TaskCommentSerializer

    def get(self, request, username, workspace_id, workboard_id, taskgroup_id, task_id):
        if not User.objects.filter(username=username).exists():
            return Response({'error': 'User is invalid.'}, status=status.HTTP_404_NOT_FOUND)

        user = User.objects.get(username=username)

        if not Workspace.objects.filter(id=workspace_id, members=user.pk).exists():
            return Response({'error': 'Workspace is invalid.'}, status=status.HTTP_404_NOT_FOUND)

        workspace = Workspace.objects.get(id=workspace_id, members=user.pk)

        if not WorkBoard.objects.filter(id=workboard_id, members=user.pk, workspace=workspace.pk).exists():
            return Response({'error': 'WorkBoard is invalid.'}, status=status.HTTP_404_NOT_FOUND)

        workboard = WorkBoard.objects.get(
            id=workboard_id, members=user.pk, workspace=workspace.pk)

        if not TaskGroup.objects.filter(id=taskgroup_id, work_board=workboard.pk).exists():
            return Response({'error': 'TaskGroup is invalid.'}, status=status.HTTP_404_NOT_FOUND)

        task_group = TaskGroup.objects.get(
            id=taskgroup_id, work_board=workboard.pk)

        if not Task.objects.filter(id=taskgroup_id, task_group=task_group.pk).exists():
            return Response({'error': 'Task is invalid.'}, status=status.HTTP_404_NOT_FOUND)

        task = Task.objects.get(id=task_id, task_group=task_group.pk)

        task_commet = [{
            'id': comment.id,
            'user': comment.user.pk,
            'task': comment.task.pk,
            'comment': comment.comment,
            'total_comment': comment.total_comment(),
            'date_created': comment.date_created,
        } for comment in task.comment.all()]

        return Response({'data': task_commet}, status=status.HTTP_200_OK)

    def post(self, request, username, workspace_id, workboard_id, taskgroup_id, task_id):
        if not User.objects.filter(username=username).exists():
            return Response({'error': 'User is invalid.'}, status=status.HTTP_404_NOT_FOUND)

        user = User.objects.get(username=username)

        if not Workspace.objects.filter(id=workspace_id, members=user.pk).exists():
            return Response({'error': 'Workspace is invalid.'}, status=status.HTTP_404_NOT_FOUND)

        workspace = Workspace.objects.get(id=workspace_id, members=user.pk)

        if not WorkBoard.objects.filter(id=workboard_id, members=user.pk, workspace=workspace.pk).exists():
            return Response({'error': 'WorkBoard is invalid.'}, status=status.HTTP_404_NOT_FOUND)

        workboard = WorkBoard.objects.get(
            id=workboard_id, members=user.pk, workspace=workspace.pk)

        if not TaskGroup.objects.filter(id=taskgroup_id, work_board=workboard.pk).exists():
            return Response({'error': 'TaskGroup is invalid.'}, status=status.HTTP_404_NOT_FOUND)

        task_group = TaskGroup.objects.get(
            id=taskgroup_id, work_board=workboard.pk)

        if not Task.objects.filter(id=taskgroup_id, task_group=task_group.pk).exists():
            return Response({'error': 'Task is invalid.'}, status=status.HTTP_404_NOT_FOUND)

        task = Task.objects.get(id=task_id, task_group=task_group.pk)

        request.data['user'] = user.pk
        request.data['task'] = task.pk

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        data = serializer.data

        return Response({'data': data}, status=status.HTTP_200_OK)


class TaskCommentDetailView(GenericAPIView):
    serializer_class = TaskCommentSerializer

    def put(self, request, username, workspace_id, workboard_id, taskgroup_id, task_id, task_comment_id):
        if not User.objects.filter(username=username).exists():
            return Response({'error': 'User is invalid.'}, status=status.HTTP_404_NOT_FOUND)

        user = User.objects.get(username=username)

        if not Workspace.objects.filter(id=workspace_id, members=user.pk).exists():
            return Response({'error': 'Workspace is invalid.'}, status=status.HTTP_404_NOT_FOUND)

        workspace = Workspace.objects.get(id=workspace_id, members=user.pk)

        if not WorkBoard.objects.filter(id=workboard_id, workspace=workspace.pk, members=user.pk).exists():
            return Response({'error': 'WorkBoard is invalid.'}, status=status.HTTP_404_NOT_FOUND)

        workboard = WorkBoard.objects.get(
            id=workboard_id, workspace=workspace.pk, members=user.pk)

        if not TaskGroup.objects.filter(id=taskgroup_id, work_board=workboard.pk).exists():
            return Response({'error': 'TaskGroup is invalid.'}, status=status.HTTP_404_NOT_FOUND)

        task_group = TaskGroup.objects.get(
            id=taskgroup_id, work_board=workboard.pk)

        if not Task.objects.filter(id=task_id, task_group=task_group.pk).exists():
            return Response({'error': 'Task is invalid.'}, status=status.HTTP_404_NOT_FOUND)

        task = Task.objects.get(id=task_id, task_group=task_group.pk)

        if not TaskComment.objects.filter(id=task_comment_id, task=task.pk).exists():
            return Response({'error': 'Task Comment is invalid.'}, status=status.HTTP_404_NOT_FOUND)

        task_comment = TaskComment.objects.get(
            id=task_comment_id, task=task.pk)

        # Only the user who comment is authorized to update their comment
        if task_comment.user.username == user.username:
            request.data['user'] = user.pk
            request.data['task'] = task.pk
            serializer = self.serializer_class(data=request.data)
            serializer.is_valid(raise_exception=True)

            task_comment.comment = serializer.data['comment']
            task_comment.save()

            return Response({'success': 'Comment updated successfully.'}, status=status.HTTP_200_OK)

        else:
            return Response({'error': 'User is not authorize for this kind of action.'}, status=status.HTTP_401_UNAUTHORIZED)

    def delete(self, request, username, workspace_id, workboard_id, taskgroup_id, task_id, task_comment_id):
        if not User.objects.filter(username=username).exists():
            return Response({'error': 'User is invalid.'}, status=status.HTTP_404_NOT_FOUND)

        user = User.objects.get(username=username)

        if not Workspace.objects.filter(id=workspace_id, members=user.pk).exists():
            return Response({'error': 'Workspace is invalid.'}, status=status.HTTP_404_NOT_FOUND)

        workspace = Workspace.objects.get(id=workspace_id, members=user.pk)

        if not WorkBoard.objects.filter(id=workboard_id, workspace=workspace.pk, members=user.pk).exists():
            return Response({'error': 'WorkBoard is invalid.'}, status=status.HTTP_404_NOT_FOUND)

        workboard = WorkBoard.objects.get(
            id=workboard_id, workspace=workspace.pk, members=user.pk)

        if not TaskGroup.objects.filter(id=taskgroup_id, work_board=workboard.pk).exists():
            return Response({'error': 'TaskGroup is invalid.'}, status=status.HTTP_404_NOT_FOUND)

        task_group = TaskGroup.objects.get(
            id=taskgroup_id, work_board=workboard.pk)

        if not Task.objects.filter(id=task_id, task_group=task_group.pk).exists():
            return Response({'error': 'Task is invalid.'}, status=status.HTTP_404_NOT_FOUND)

        task = Task.objects.get(id=task_id, task_group=task_group.pk)

        if not TaskComment.objects.filter(id=task_comment_id, task=task.pk).exists():
            return Response({'error': 'Task Comment is invalid.'}, status=status.HTTP_404_NOT_FOUND)

        task_comment = TaskComment.objects.get(
            id=task_comment_id, task=task.pk)

        # Leader and user who comment is authorized to delete the comment
        if task_comment.user.username == user.username or workspace.leader.username == user.username:
            task_comment.delete()

            return Response({'success': 'Comment deleted successfully'}, status=status.HTTP_200_OK)

        else:
            return Response({'error': 'User is not authorize for this kind of action.'}, status=status.HTTP_401_UNAUTHORIZED)
