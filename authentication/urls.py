from django.urls import path
from .views import UserRegisterView, UserEmailVerificationView, UserLoginView


urlpatterns = [
    path('register/', UserRegisterView.as_view(), name='register'),
    path('verify-email/<token>/',
         UserEmailVerificationView.as_view(), name='verify-email'),
    path('login/', UserLoginView.as_view(), name='login')
]
