from django.urls import path
from .views import (UserDetailView, UserDisableAccountView,
                    UserRecoverAccountView, UserDeleteAccountView)


urlpatterns = [
    path('details/<username>/', UserDetailView.as_view(), name='update-user'),
    path('disable-account/<username>/',
         UserDisableAccountView.as_view(), name='disable-account'),
    path('recover-account/<username>/',
         UserRecoverAccountView.as_view(), name='recover-account'),
    path('delete-account/<username>/',
         UserDeleteAccountView.as_view(), name='delete-account')
]
