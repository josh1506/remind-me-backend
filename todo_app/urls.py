from django.urls import path
from .views import ToDoListView, ToDoListDetailView


urlpatterns = [
    path('list/<username>/', ToDoListView.as_view(), name='list'),
    path('list/<username>/<int:todo_id>/',
         ToDoListDetailView.as_view(), name='todo-details')
]
