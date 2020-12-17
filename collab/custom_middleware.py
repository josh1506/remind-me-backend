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
            id=workspace_id)

        if not workspace.exists():
            raise ValidationError({'error': 'Workspace is invalid.'}, 404)

        if not workspace[0].members.filter(id=user.pk).exists():
            raise ValidationError({'error': 'User is not in workspace'}, 400)

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
            id=workboard_id, workspace=workspace.pk)

        if not workboard.exists():
            raise ValidationError({'error': 'Workboard is invalid.'}, 404)

        if not workboard[0].members.filter(id=user.pk).exists():
            raise ValidationError({'error': 'User is not in workboard'}, 400)

        return workboard[0]

    @staticmethod
    def validate_task_group(workboard, taskgroup_id):
        taskgroup = workboard.task_group.filter(id=taskgroup_id)

        if not taskgroup.exists():
            raise ValidationError({'error': 'Taskgroup is invalid.'}, 404)

        return taskgroup[0]

    @staticmethod
    def validate_task(taskgroup, task_id):
        task = taskgroup.task.filter(id=task_id)

        if not task.exists():
            raise ValidationError({'error': 'Task is invalid.'}, 404)

        return task[0]

    @staticmethod
    def validate_comment(task, comment_id):
        comment = task.comment.filter(id=comment_id)

        if not comment.exists():
            raise ValidationError({'error': 'Comment is invalid.'}, 404)

        return comment[0]

    @staticmethod
    def is_leader(user, workspace):
        '''
        user - user data \n
        workspace - workspace data \n

        Validating if user is the leader in the current
        workspace if not it will return 401 error which is
        unauthorized
        '''
        if not user.username == workspace.leader.username:
            raise ValidationError(
                {'error': 'User is not authorize for this kind of action.'}, 401)
