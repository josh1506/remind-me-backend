from django.db import models
from users.models import User


# Create your models here.

class ToDo(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='todo')
    title = models.CharField(max_length=255, blank=False)
    image = models.ImageField(upload_to="todo_img", blank=True)
    complete = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now=True, editable=False)

    def __str__(self):
        return self.title


class ToDoTask(models.Model):
    todo = models.ForeignKey(
        ToDo, on_delete=models.CASCADE, related_name='task')
    name = models.CharField(max_length=255, blank=False)
    complete = models.BooleanField(default=False)

    def __str__(self):
        return self.name
