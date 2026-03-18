"""
URLs for user authentication and management
"""
from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from .views import (
    RegisterView, LoginView, LogoutView,
    UserProfileView, PasswordResetView,
    PasswordChangeView, VerifyUserView
)

urlpatterns = [
    # Authentication
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('logout/', LogoutView.as_view(), name='logout'),
    
    # User profile
    path('profile/', UserProfileView.as_view(), name='profile'),
    
    # Password management
    path('password/reset/', PasswordResetView.as_view(), name='password_reset'),
    path('password/change/', PasswordChangeView.as_view(), name='password_change'),
    
    # Verification
    path('verify/', VerifyUserView.as_view(), name='verify_user'),
]