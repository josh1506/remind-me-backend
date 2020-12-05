from django.contrib import admin

from .models import Workspace, WorkBoard, TaskGroup, Task


# Register your models here.

@admin.register(Workspace)
class WorkspaceAdmin(admin.ModelAdmin):
    list_display = ['title', 'leader', 'link', 'date_created']
    search_fields = ['title', 'leader']
    list_filter = ['leader', 'date_created']
    exclude = ('date_created', )


@admin.register(WorkBoard)
class WorkBoardAdmin(admin.ModelAdmin):
    list_display = ['title', 'privacy', 'date_created']
    search_fields = ['title', 'privacy']
    list_filter = ['privacy', 'date_created']
    exclude = ('date_created', )


@admin.register(TaskGroup)
class TaskGroupAdmin(admin.ModelAdmin):
    list_display = ['title', 'date_created']
    search_fields = ['title']
    list_filter = ['date_created']
    exclude = ('date_created', )


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ['task', 'status', 'due_date', 'date_created']
    search_fields = ['task', 'status']
    list_filter = ['status', 'date_created']
    exclude = ('date_created', )
