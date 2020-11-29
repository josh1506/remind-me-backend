from django.urls import path
from .views import (UserRegisterView, UserEmailVerificationView, UserLoginView,
                    UserRequestPasswordResetView, VerifyPasswordResetTokenView, UserSetNewPasswordView)


urlpatterns = [
    path('register/', UserRegisterView.as_view(), name='register'),
    path('verify-email/<token>/',
         UserEmailVerificationView.as_view(), name='verify-email'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('request-password-reset/',
         UserRequestPasswordResetView.as_view(), name='request-password-reset'),
    path('validate-password-reset/<uidb64>/<token>/', VerifyPasswordResetTokenView.as_view(),
         name='validate-password-reset'),
    path('set-new-password/', UserSetNewPasswordView.as_view(),
         name='set-new-password')
]
