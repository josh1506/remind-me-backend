from rest_framework import serializers
from rest_framework.serializers import ValidationError

from .models import (Workspace, WorkBoard, TaskGroup, Task, TaskComment)
from .custom_middleware import Custom_Middleware as middleware


class WorkspaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Workspace
        fields = ['id', 'title', 'members', 'leader', 'link']

    def get_workspace_list(self, username):
        user = middleware.validate_user(username)

        return [{
            'title': workspace.title,
            'link': workspace.link,
            'leader': workspace.leader.username,
            'members-count': workspace.members_count()
        } for workspace in user.workspace.all()]

    def update_workspace(self, workspace, data):
        workspace.title = data['title']
        workspace.save()


class WorkBoardSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkBoard
        fields = ['id', 'title', 'members', 'workspace', 'privacy']

    def get_workboard_list(self, user, workspace):
        if user.username == workspace.leader.username:
            return [{
                'id': workboard.pk,
                'title': workboard.title,
                'privacy': workboard.privacy,
                'members-count': workboard.members_count()
            } for workboard in workspace.board.all()]

        else:
            return [{
                'id': workboard.pk,
                'title': workboard.title,
                'privacy': workboard.privacy,
                'members-count': workboard.members_count()
            } for workboard in workspace.board.filter(members=user.pk)]

    def validate(self, attrs):
        username = attrs.get('username', '')
        workspace_leader = attrs.get('workspace-leader', '')

        # Only leader is authorized to create new workboard inside their workspace
        if not username == workspace_leader:
            return ValidationError({'error': 'User is not authorize for this kind of action.'}, 401)

        return attrs

    def update_workboard(self, workboard, data):
        workboard.title = data['title']
        workboard.privacy = data['privacy']
        workboard.save()


class TaskGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskGroup
        fields = ['id', 'title', 'work_board']

    def get_taskgroup_list(self, workboard):
        return [{
            'id': task_group.pk,
            'title': task_group.title,
            'progress': task_group.progress()
        } for task_group in workboard.task_group.all()]


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['id', 'task_group', 'task', 'status', 'due_date']

    def get_task_list(self, task_group):
        return [{
                'id': task.id,
                'task': task.task,
                'people': [{
                    'id': people.pk,
                    'username': people.username
                } for people in task.people.all()],
                'status': task.status,
                'due_date': task.due_date,
                } for task in task_group.task.all()]


class TaskCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskComment
        fields = ['id', 'user', 'task', 'comment',
                  'total_comment', 'date_created']

    def get_comments(self, task):
        return [{
            'id': comment.id,
            'user': comment.user.pk,
            'task': comment.task.pk,
            'comment': comment.comment,
            'total_comment': comment.total_comment(),
            'date_created': comment.date_created,
        } for comment in task.comment.all()]
