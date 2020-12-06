from django.urls import path
from .views import WorkspaceListView, WorkspaceView, WorkBoardListView


urlpatterns = [
    path('workspace-list/<username>/',
         WorkspaceListView.as_view(), name='workspace-list'),
    path('workspace-detail/<username>/<collab_id>/',
         WorkspaceView.as_view(), name='workspace-detail'),
    path('workboard-list/<username>/<workspace_id>/',
         WorkBoardListView.as_view(), name='workboard-list')
]
