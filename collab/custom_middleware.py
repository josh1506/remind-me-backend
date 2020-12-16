from rest_framework.serializers import ValidationError

from users.models import User
from .models import (Workspace, WorkBoard,
                     TaskGroup, Task, TaskComment)


class Custom_Middleware:
    @staticmethod
    def validate_user(username):
        '''
        username - Input username from url params. \n

        If username is invalid it will return 
        an error with a status of 404.
        '''

        user = User.objects.filter(username=username)

        if not user.exists():
            raise ValidationError({'error': 'User is invalid.'}, 404)

        return user[0]

    @staticmethod
    def validate_workspace(user, workspace_id):
        '''
        workspace_id - Input workspace id from url params. \n
        user - Input user data. \n

        If a workspace doesn't match user in members
        it will return an error with a status of 404.
        '''

        workspace = Workspace.objects.filter(
            id=workspace_id, members=user.pk)

        if not workspace.exists():
            raise ValidationError({'error': 'Workspace is invalid.'}, 404)

        return workspace[0]

    @staticmethod
    def validate_workboard(user, workspace, workboard_id):
        '''
        workboard_id - Input workboard id from url params. \n
        user - Input user data. \n
        workspace - Input workspace data. \n

        If a workboard doesn't match any user in members
        it will return an error with a status of 404.
        '''

        workboard = workspace.board.filter(
            id=workboard_id, workspace=workspace.pk, members=user.pk)

        if not workboard.exists():
            raise ValidationError({'error': 'Workboard is invalid.'}, 404)

        return workboard[0]

    def validate_task_group(self):
        pass

    def validate_task(self):
        pass

    @staticmethod
    def is_leader(user, workspace):
        if not user.username == workspace.leader.username:
            raise ValidationError(
                {'error': 'User is not authorize for this kind of action.'}, 401)
