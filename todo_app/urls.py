from django.urls import path
from .views import ToDoListView


urlpatterns = [
    path('list/<username>/', ToDoListView.as_view(), name='list')
]
