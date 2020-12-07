from django.db import models
from users.models import User


# Create your models here.

class Workspace(models.Model):
    title = models.CharField(max_length=255, blank=False, default='Workspace')
    members = models.ManyToManyField(
        User, related_name='workspace', blank=True)
    leader = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='owned_workspace')
    link = models.CharField(max_length=255)
    date_created = models.DateTimeField(auto_now=True)

    def members_count(self):
        return len(self.members.all())


class WorkBoard(models.Model):
    PRIVACY_TYPE = [('public', 'Public'), ('private', 'Private')]

    workspace = models.ForeignKey(
        Workspace, on_delete=models.CASCADE, related_name='board')
    title = models.CharField(max_length=255, default='Work Board')
    privacy = models.CharField(
        max_length=255, choices=PRIVACY_TYPE, default='public')
    members = models.ManyToManyField(
        User, related_name='work_board', blank=True)
    date_created = models.DateTimeField(auto_now=True)

    def members_count(self):
        return len(self.members.all())


class TaskGroup(models.Model):
    work_board = models.ForeignKey(
        WorkBoard, on_delete=models.CASCADE, related_name='task_group')
    title = models.CharField(max_length=255, blank=False)
    date_created = models.DateTimeField(auto_now=True)

    def progress(self):
        task_list = Task.objects.filter(task_group=self)
        total_task = len(task_list)
        task_completed = len(Task.objects.filter(status='done'))

        if not total_task <= 0:
            return int((task_completed/total_task) * 100)

        return 100


class Task(models.Model):
    STATUS_TYPE = [('on-going', 'On progress'), ('stuck', 'Stuck'),
                   ('done', 'Finished'), ('queue', 'Queue')]

    task_group = models.ForeignKey(
        TaskGroup, on_delete=models.CASCADE, related_name='task')
    task = models.CharField(max_length=255, default='Undefined task')
    people = models.ManyToManyField(User, related_name='task', blank=True)
    status = models.CharField(
        max_length=255, choices=STATUS_TYPE, default='queue')
    due_date = models.DateField()
    date_created = models.DateTimeField(auto_now=True)


class TaskComment(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='comment')
    task = models.ForeignKey(
        Task, on_delete=models.CASCADE, related_name='comment')
    comment = models.TextField()
    date_created = models.DateTimeField(auto_now=True)

    def total_comment(self):
        return len(Task.objects.filter(id=self.task.pk))
