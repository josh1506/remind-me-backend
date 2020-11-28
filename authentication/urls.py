from django.urls import path
from .views import UserRegisterView, UserEmailVerificationView


urlpatterns = [
    path('register/', UserRegisterView.as_view(), name='register'),
    path('verify-email/<token>/',
         UserEmailVerificationView.as_view(), name='verify-email')
]
