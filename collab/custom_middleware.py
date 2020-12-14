from rest_framework.serializers import ValidationError

from users.models import User
from .models import (Workspace, WorkBoard,
                     TaskGroup, Task, TaskComment)


class Custom_Middleware:
    @staticmethod
    def validate_user(username):
        user = User.objects.filter(username=username)

        if not user.exists():
            raise ValidationError({'error': 'User is invalid.'}, 404)

        return user[0]

    @staticmethod
    def validate_workspace(members_id, workspace_id):
        '''
        members - user primary key or id
        '''
        workspace = Workspace.objects.filter(
            id=workspace_id, members=members_id)

        if not workspace.exists():
            raise ValidationError({'error': 'Workspace is invalid.'}, 404)

        return workspace[0]

    @staticmethod
    def validate_workboard(members_id, workspace_id, workboard_id):
        '''
        members - user primary key or id
        workspace_id - workspace primary key or id
        '''
        workboard = WorkBoard.objects.filter(
            id=workboard_id, workspace=workspace_id, members=members_id)

        if not workboard.exists():
            raise ValidationError({'error': 'Workboard is invalid.'}, 404)

        return workboard[0]

    def validate_task_group(self):
        pass

    def validate_task(self):
        pass
