from django.urls import path
from .views import ToDoListView, ToDoListDetailView, ToDoTaskDetailView, ToDoTaskView


urlpatterns = [
    path('list/<username>/', ToDoListView.as_view(), name='list'),
    path('list/<username>/<todo_id>/',
         ToDoListDetailView.as_view(), name='todo-details'),
    path('task/<username>/<todo_id>/', ToDoTaskView.as_view(), name='task'),
    path('task-detail/<username>/<todo_id>/<task_id>/',
         ToDoTaskDetailView.as_view(), name='task-detail')
]
