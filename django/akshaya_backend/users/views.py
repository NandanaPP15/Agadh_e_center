"""
Views for User authentication and management
"""
from rest_framework import status, generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

from .serializers import (
    UserSerializer, RegisterSerializer, LoginSerializer,
    PasswordResetSerializer, PasswordChangeSerializer
)
from .models import UserProfile

User = get_user_model()

class RegisterView(generics.CreateAPIView):
    """Register new user"""
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        
        # Create user profile
        UserProfile.objects.create(user=user)
        
        # Generate tokens
        refresh = RefreshToken.for_user(user)
        
        return Response({
            'user': UserSerializer(user).data,
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'message': _('Registration successful')
        }, status=status.HTTP_201_CREATED)

class LoginView(TokenObtainPairView):
    """User login view with custom response"""
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        
        if response.status_code == 200:
            # Get user data
            username = request.data.get('username')
            user = User.objects.get(username=username)
            
            # Add user data to response
            response.data['user'] = UserSerializer(user).data
            response.data['message'] = _('Login successful')
        
        return response

class LogoutView(APIView):
    """Logout user by blacklisting refresh token"""
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request):
        try:
            refresh_token = request.data.get("refresh")
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"message": _("Logout successful")}, status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

class UserProfileView(generics.RetrieveUpdateAPIView):
    """Get or update user profile"""
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_object(self):
        return self.request.user
    
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        
        # Update profile if profile data is provided
        profile_data = request.data.get('profile')
        if profile_data and hasattr(instance, 'profile'):
            profile_serializer = UserProfileSerializer(instance.profile, data=profile_data, partial=partial)
            if profile_serializer.is_valid():
                profile_serializer.save()
        
        return Response(serializer.data)

class PasswordResetView(APIView):
    """Request password reset"""
    permission_classes = [permissions.AllowAny]
    
    def post(self, request):
        serializer = PasswordResetSerializer(data=request.data)
        if serializer.is_valid():
            # In production, send email with reset link
            return Response({"message": _("Password reset instructions sent to email")})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PasswordChangeView(APIView):
    """Change password"""
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request):
        serializer = PasswordChangeSerializer(data=request.data)
        if serializer.is_valid():
            user = request.user
            if not user.check_password(serializer.validated_data['old_password']):
                return Response({"old_password": _("Wrong password")}, 
                              status=status.HTTP_400_BAD_REQUEST)
            
            user.set_password(serializer.validated_data['new_password'])
            user.save()
            return Response({"message": _("Password changed successfully")})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class VerifyUserView(APIView):
    """Verify user identity"""
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request):
        user = request.user
        verification_type = request.data.get('type')
        
        if verification_type == 'phone':
            # Phone verification logic
            user.is_phone_verified = True
            message = _("Phone number verified successfully")
        elif verification_type == 'email':
            # Email verification logic
            user.is_email_verified = True
            message = _("Email verified successfully")
        else:
            return Response({"error": _("Invalid verification type")}, 
                          status=status.HTTP_400_BAD_REQUEST)
        
        user.save()
        return Response({"message": message})