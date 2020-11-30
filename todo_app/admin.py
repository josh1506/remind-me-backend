from django.contrib import admin
from .models import ToDo, ToDoTask


# Register your models here.
@admin.register(ToDo)
class ToDoAdmin(admin.ModelAdmin):
    list_display = ['title', 'complete', 'date_created']
    list_filter = ['date_created', ]
    search_fields = ['user', 'title']


@admin.register(ToDoTask)
class ToDoTaskAdmin(admin.ModelAdmin):
    list_display = ['name', 'complete']
    search_fields = ['name']
