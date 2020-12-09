from rest_framework import serializers

from .models import (Workspace, WorkBoard, TaskGroup, Task, TaskComment)


class WorkspaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Workspace
        fields = ['id', 'title', 'leader', 'link']

    def validate(self, attrs):
        title = attrs.get('title', '')
        leader = attrs.get('leader', '')
        link = attrs.get('link', '')

        return attrs

    def create(self, validated_data):
        return Workspace.objects.create(**validated_data)


class WorkBoardSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkBoard
        fields = ['id', 'title', 'workspace', 'privacy']

    def create(self, validated_data):
        return WorkBoard.objects.create(**validated_data)


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
