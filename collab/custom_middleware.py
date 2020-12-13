from rest_framework.serializers import ValidationError

from users.models import User
from .models import Workspace


class Custom_Middleware:
    @staticmethod
    def validate_user(username):
        user = User.objects.filter(username=username)

        if not user.exists():
            raise ValidationError({'error': 'User is invalid.'}, 404)

        return user[0]

    @staticmethod
    def validate_workspace(members, workspace_id):
        '''
        members - only require user primary key
        '''
        workspace = Workspace.objects.filter(id=workspace_id, members=members)

        if not workspace.exists():
            raise ValidationError({'error': 'Workspace is invalid.'}, 404)

        return workspace[0]

    def validate_workboard(self):
        pass

    def validate_task_group(self):
        pass

    def validate_task(self):
        pass
