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
                         TaskCommentSerializer, JoinLeaveSerializer)


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
        request.data['members'] = [user.pk]

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
        request.data['members'] = [user.pk]
        request.data['link'] = generate_link()

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
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
        user = middleware.validate_user(username)
        workspace = middleware.validate_workspace(
            user=user, workspace_id=workspace_id)
        workboard = middleware.validate_workboard(
            user=user, workspace=workspace, workboard_id=workboard_id)
        task_group = middleware.validate_task_group(
            workboard=workboard, taskgroup_id=taskgroup_id)

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
        user = middleware.validate_user(username)
        workspace = middleware.validate_workspace(
            user=user, workspace_id=workspace_id)
        workboard = middleware.validate_workboard(
            user=user, workspace=workspace, workboard_id=workboard_id)
        task_group = middleware.validate_task_group(
            workboard=workboard, taskgroup_id=taskgroup_id)

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
        user = middleware.validate_user(username)
        workspace = middleware.validate_workspace(
            user=user, workspace_id=workspace_id)
        workboard = middleware.validate_workboard(
            user=user, workspace=workspace, workboard_id=workboard_id)
        task_group = middleware.validate_task_group(
            workboard=workboard, taskgroup_id=taskgroup_id)
        task = middleware.validate_task(task_id=task_id, taskgroup=task_group)

        # Only leader is authorized to delete task
        middleware.is_leader(user=user, workspace=workspace)
        task.delete()

        return Response({'success': 'Task deleted successfully.'}, status=status.HTTP_200_OK)


class TaskCommentListView(GenericAPIView):
    serializer_class = TaskCommentSerializer

    def get(self, request, username, workspace_id, workboard_id, taskgroup_id, task_id):
        user = middleware.validate_user(username)
        workspace = middleware.validate_workspace(
            user=user, workspace_id=workspace_id)
        workboard = middleware.validate_workboard(
            user=user, workspace=workspace, workboard_id=workboard_id)
        task_group = middleware.validate_task_group(
            workboard=workboard, taskgroup_id=taskgroup_id)
        task = middleware.validate_task(task_id=task_id, taskgroup=task_group)

        serializer = self.serializer_class()
        task_commet = serializer.get_comments(task)

        return Response({'data': task_commet}, status=status.HTTP_200_OK)

    def post(self, request, username, workspace_id, workboard_id, taskgroup_id, task_id):
        user = middleware.validate_user(username=username)
        workspace = middleware.validate_workspace(
            workspace_id=workspace_id, user=user)
        workboard = middleware.validate_workboard(
            workboard_id=workboard_id, user=user, workspace=workspace)
        task_group = middleware.validate_task_group(
            taskgroup_id=taskgroup_id, workboard=workboard)
        task = middleware.validate_task(task_id=task_id, taskgroup=task_group)

        request.data['user'] = user.pk
        request.data['task'] = task.pk

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        comment = serializer.data

        return Response({'data': comment}, status=status.HTTP_200_OK)


class TaskCommentDetailView(GenericAPIView):
    serializer_class = TaskCommentSerializer

    def put(self, request, username, workspace_id, workboard_id, taskgroup_id, task_id, comment_id):
        user = middleware.validate_user(username=username)
        workspace = middleware.validate_workspace(
            workspace_id=workspace_id, user=user)
        workboard = middleware.validate_workboard(
            workboard_id=workboard_id, user=user, workspace=workspace)
        task_group = middleware.validate_task_group(
            taskgroup_id=taskgroup_id, workboard=workboard)
        task = middleware.validate_task(task_id=task_id, taskgroup=task_group)
        task_comment = middleware.validate_comment(
            comment_id=comment_id, task=task)

        # Only the user who comment is authorized to update their comment
        middleware.is_leader(user=user, workspace=workspace)

        request.data['user'] = user.pk
        request.data['task'] = task.pk
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        task_comment.comment = serializer.data['comment']
        task_comment.save()

        return Response({'success': 'Comment updated successfully.'}, status=status.HTTP_200_OK)

    def delete(self, request, username, workspace_id, workboard_id, taskgroup_id, task_id, comment_id):
        user = middleware.validate_user(username)
        workspace = middleware.validate_workspace(
            user=user, workspace_id=workspace_id)
        workboard = middleware.validate_workboard(
            user=user, workspace=workspace, workboard_id=workboard_id)
        task_group = middleware.validate_task_group(
            workboard=workboard, taskgroup_id=taskgroup_id)
        task = middleware.validate_task(task_id=task_id, taskgroup=task_group)
        task_comment = middleware.validate_comment(
            comment_id=comment_id, task=task)

        # Only the user who comment is authorized to update their comment
        middleware.is_leader(user=user, workspace=workspace)
        task_comment.delete()

        return Response({'success': 'Comment deleted successfully'}, status=status.HTTP_200_OK)


# Joining and Leaving in workboard

class JoinWorkboardView(GenericAPIView):
    serializer_class = JoinLeaveSerializer

    def post(self, request, username):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.data

        user = middleware.validate_user(username)
        workboard = middleware.validate_link(data['link'])
        workspace = Workspace.objects.get(id=workboard.workspace.pk)

        workspace.members.add(user.pk)
        workboard.members.add(user.pk)

        return Response({'success': 'Join successfuly.'}, status=status.HTTP_200_OK)


class LeaveWorkboardView(GenericAPIView):
    def delete(self, request, username, workspace_id, workboard_id):
        user = middleware.validate_user(username)
        workspace = middleware.validate_workspace(
            user=user, workspace_id=workspace_id)
        workboard = middleware.validate_workboard(
            user=user, workspace=workspace, workboard_id=workboard_id)
        workboard.members.remove(user.pk)

        return Response({'success': 'Leave successfuly in workboard.'}, status=status.HTTP_200_OK)


class LeaveWorkspaceView(GenericAPIView):
    def delete(self, request, username, workspace_id):
        user = middleware.validate_user(username)
        workspace = middleware.validate_workspace(
            workspace_id=workspace_id, user=user)
        middleware.validate_user_leave(user=user, workspace=workspace)

        [workboard.members.remove(user.pk)
         for workboard in workspace.board.all()]

        workspace.members.remove(user.pk)

        return Response({'success': 'Leave successfuly in workspace.'}, status=status.HTTP_200_OK)
