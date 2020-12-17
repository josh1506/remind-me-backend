from django.urls import path
from .views import (WorkspaceListView, WorkspaceDetailView,
                    WorkBoardListView, WorkBoardDetailView,
                    TaskGroupListView, TaskGroupDetailView,
                    TaskListView, TaskDetailView,
                    TaskCommentListView, TaskCommentDetailView)


urlpatterns = [
    path('workspace-list/<username>/',
         WorkspaceListView.as_view(), name='workspace-list'),
    path('workspace-detail/<username>/<workspace_id>/',
         WorkspaceDetailView.as_view(), name='workspace-detail'),

    path('workboard-list/<username>/<workspace_id>/',
         WorkBoardListView.as_view(), name='workboard-list'),
    path('workboard-detail/<username>/<workspace_id>/<workboard_id>/',
         WorkBoardDetailView.as_view(), name='workboard-detail'),

    path('taskgroup-list/<username>/<workspace_id>/<workboard_id>/',
         TaskGroupListView.as_view(), name='taskgroup-list'),
    path('taskgroup-detail/<username>/<workspace_id>/<workboard_id>/<taskgroup_id>/',
         TaskGroupDetailView.as_view(), name='taskgroup-detail'),

    path('task-list/<username>/<workspace_id>/<workboard_id>/<taskgroup_id>/',
         TaskListView.as_view(), name='task-list'),
    path('task-detial/<username>/<workspace_id>/<workboard_id>/<taskgroup_id>/<task_id>/',
         TaskDetailView.as_view(), name='task-detail'),

    path('task-comment-list/<username>/<workspace_id>/<workboard_id>/<taskgroup_id>/<task_id>/',
         TaskCommentListView.as_view(), name='task-comment-list'),
    path('task-comment-detail/<username>/<workspace_id>/<workboard_id>/<taskgroup_id>/<task_id>/<comment_id>/',
         TaskCommentDetailView.as_view(), name='task-comment-detail')
]
