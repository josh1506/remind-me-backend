from django.urls import path
from .views import (WorkspaceListView, WorkspaceView,
                    WorkBoardListView, WorkBoardDetailView, TaskGroupListView)


urlpatterns = [
    path('workspace-list/<username>/',
         WorkspaceListView.as_view(), name='workspace-list'),
    path('workspace-detail/<username>/<workspace_id>/',
         WorkspaceView.as_view(), name='workspace-detail'),

    path('workboard-list/<username>/<workspace_id>/',
         WorkBoardListView.as_view(), name='workboard-list'),
    path('workboard-detail/<username>/<workspace_id>/<workboard_id>/',
         WorkBoardDetailView.as_view(), name='workboard-detail'),

    path('taskgroup-list/<username>/<workspace_id>/<workboard_id>/',
         TaskGroupListView.as_view(), name='taskgroup-list'),
]
