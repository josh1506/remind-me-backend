from django.urls import path
from .views import UserDetailView


urlpatterns = [
    path('details/<username>/', UserDetailView.as_view(), name='update-user')
]
