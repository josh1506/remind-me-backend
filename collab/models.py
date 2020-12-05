from django.db import models
from users.models import User


# Create your models here.

class Workspace(models.Model):
    title = models.CharField(max_length=255, blank=False, default='Workspace')
    members = models.ManyToManyField(User, related_name='workspace')
    leader = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='owned_workspace')
    link = models.CharField(max_length=255)
    date_created = models.DateTimeField(auto_now=True)

    def members_count(self):
        pass


class WorkBoard(models.Model):
    PRIVACY_TYPE = [('public', 'Public'), ('private', 'Private')]

    workspace = models.ForeignKey(
        Workspace, on_delete=models.CASCADE, related_name='board')
    title = models.CharField(max_length=255, default='Work Board')
    privacy = models.CharField(
        max_length=255, choices=PRIVACY_TYPE, default='public')
    members = models.ManyToManyField(User, related_name='work_board')
    date_created = models.DateTimeField(auto_now=True)

    def members_count(self):
        pass


class TaskGroup(models.Model):
    work_board = models.ForeignKey(
        WorkBoard, on_delete=models.CASCADE, related_name='task_group')
    title = models.CharField(max_length=255, blank=False)
    date_created = models.DateTimeField(auto_now=True)

    def progress(self):
        pass


class Task(models.Model):
    STATUS_TYPE = [('on-going', 'On progress'), ('stuck', 'Stuck'),
                   ('done', 'Finished'), ('queue', 'Queue')]

    task_group = models.ForeignKey(
        TaskGroup, on_delete=models.CASCADE, related_name='task')
    task = models.CharField(max_length=255, default='Undefined task')
    comment = models.TextField()
    people = models.ManyToManyField(User, related_name='task')
    status = models.CharField(
        max_length=255, choices=STATUS_TYPE, default='queue')
    due_date = models.DateField()
    date_created = models.DateTimeField(auto_now=True)
