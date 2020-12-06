from rest_framework import serializers

from .models import Workspace, WorkBoard, TaskGroup, Task


class WorkspaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Workspace
        fields = ['title', 'leader', 'link']

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
        fields = ['title', 'privacy']


class TaskGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskGroup
        fields = ['title']


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['task', 'comment', 'status', 'due_date']
