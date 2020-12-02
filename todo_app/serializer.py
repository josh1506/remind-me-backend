from rest_framework import serializers
from .models import ToDo, ToDoTask


class ToDoTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = ToDoTask
        fields = ['id', 'todo', 'name', 'complete']


class ToDoSerializer(serializers.ModelSerializer):
    task = ToDoTaskSerializer(required=False, many=True)
    image = serializers.ImageField(required=False)

    class Meta:
        model = ToDo
        fields = ['id', 'title', 'user', 'task',
                  'image', 'complete', 'date_created']

    def update_todo_details(self, validate_data, todo_id):
        user = validate_data['user']
        todo_id = validate_data['id']

        todo = ToDo.objects.get(user=user, id=todo_id)
        print(todo)
