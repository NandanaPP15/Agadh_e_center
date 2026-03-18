"""
Serializers for User models
"""
from rest_framework import serializers
from django.contrib.auth import authenticate
from django.utils.translation import gettext_lazy as _
from .models import User, UserProfile

class UserProfileSerializer(serializers.ModelSerializer):
    """Serializer for UserProfile"""
    class Meta:
        model = UserProfile
        fields = [
            'photo', 'date_of_birth', 'gender', 'education', 
            'occupation', 'family_members', 'ration_card_number',
            'pan_number', 'voter_id', 'driving_license'
        ]
        read_only_fields = ['created_at', 'updated_at']

class UserSerializer(serializers.ModelSerializer):
    """Serializer for User model"""
    profile = UserProfileSerializer(read_only=True)
    password = serializers.CharField(write_only=True, required=False)
    
    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'first_name', 'last_name',
            'user_type', 'phone', 'aadhaar_number', 'address',
            'district', 'pincode', 'preferred_language',
            'is_phone_verified', 'is_email_verified',
            'date_joined', 'last_login', 'profile', 'password'
        ]
        read_only_fields = ['date_joined', 'last_login', 'is_phone_verified', 'is_email_verified']
    
    def create(self, validated_data):
        """Create user with encrypted password"""
        password = validated_data.pop('password', None)
        user = User(**validated_data)
        if password:
            user.set_password(password)
        user.save()
        return user
    
    def update(self, instance, validated_data):
        """Update user"""
        password = validated_data.pop('password', None)
        if password:
            instance.set_password(password)
        return super().update(instance, validated_data)

class RegisterSerializer(serializers.ModelSerializer):
    """Serializer for user registration"""
    password = serializers.CharField(write_only=True, min_length=6)
    confirm_password = serializers.CharField(write_only=True, min_length=6)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'confirm_password', 
                 'first_name', 'last_name', 'phone', 'preferred_language']
    
    def validate(self, data):
        """Validate registration data"""
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError({"password": "Passwords don't match."})
        
        if User.objects.filter(username=data['username']).exists():
            raise serializers.ValidationError({"username": "Username already exists."})
        
        if User.objects.filter(email=data['email']).exists():
            raise serializers.ValidationError({"email": "Email already exists."})
        
        return data
    
    def create(self, validated_data):
        """Create new user"""
        validated_data.pop('confirm_password')
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
            phone=validated_data.get('phone', ''),
            preferred_language=validated_data.get('preferred_language', 'en')
        )
        return user

class LoginSerializer(serializers.Serializer):
    """Serializer for user login"""
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)
    
    def validate(self, data):
        """Validate login credentials"""
        username = data.get('username')
        password = data.get('password')
        
        if username and password:
            user = authenticate(username=username, password=password)
            if user:
                if not user.is_active:
                    raise serializers.ValidationError(_("User account is disabled."))
                data['user'] = user
            else:
                raise serializers.ValidationError(_("Unable to log in with provided credentials."))
        else:
            raise serializers.ValidationError(_("Must include 'username' and 'password'."))
        
        return data

class PasswordResetSerializer(serializers.Serializer):
    """Serializer for password reset"""
    email = serializers.EmailField()
    
    def validate_email(self, value):
        """Validate email exists"""
        if not User.objects.filter(email=value).exists():
            raise serializers.ValidationError(_("No user found with this email address."))
        return value

class PasswordChangeSerializer(serializers.Serializer):
    """Serializer for password change"""
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True, min_length=6)
    confirm_password = serializers.CharField(required=True, min_length=6)
    
    def validate(self, data):
        """Validate password change"""
        if data['new_password'] != data['confirm_password']:
            raise serializers.ValidationError({"new_password": "Passwords don't match."})
        return data