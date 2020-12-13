from rest_framework import serializers

from .models import (Workspace, WorkBoard, TaskGroup, Task, TaskComment)
from .custom_middleware import Custom_Middleware as middleware


class WorkspaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Workspace
        fields = ['id', 'title', 'leader', 'link']

    def get_workspace_list(self, username):
        user = middleware.validate_user(username)

        return [{
            'title': workspace.title,
            'link': workspace.link,
            'leader': workspace.leader.username,
            'members-count': workspace.members_count()
        } for workspace in user.workspace.all()]


class WorkBoardSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkBoard
        fields = ['id', 'title', 'workspace', 'privacy']


class TaskGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskGroup
        fields = ['id', 'title', 'work_board']


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['id', 'task_group', 'task', 'status', 'due_date']


class TaskCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskComment
        fields = ['id', 'user', 'task', 'comment',
                  'total_comment', 'date_created']
