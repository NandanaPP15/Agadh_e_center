"""
User models for Agadh platform
"""
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

class User(AbstractUser):
    """Custom User Model for Agadh"""
    # User types
    CITIZEN = 'citizen'
    EMPLOYEE = 'employee'
    ADMIN = 'admin'
    
    USER_TYPE_CHOICES = [
        (CITIZEN, 'Citizen'),
        (EMPLOYEE, 'Akshaya Employee'),
        (ADMIN, 'Administrator'),
    ]
    
    # Additional fields
    user_type = models.CharField(
        max_length=20,
        choices=USER_TYPE_CHOICES,
        default=CITIZEN
    )
    phone = models.CharField(max_length=15, blank=True, null=True)
    aadhaar_number = models.CharField(max_length=12, blank=True, null=True, unique=True)
    address = models.TextField(blank=True, null=True)
    district = models.CharField(max_length=100, blank=True, null=True)
    pincode = models.CharField(max_length=10, blank=True, null=True)
    preferred_language = models.CharField(
        max_length=10,
        choices=[('en', 'English'), ('ml', 'Malayalam')],
        default='en'
    )
    
    # Verification fields
    is_phone_verified = models.BooleanField(default=False)
    is_email_verified = models.BooleanField(default=False)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')
        ordering = ['-date_joined']
    
    def __str__(self):
        return f"{self.username} ({self.get_user_type_display()})"
    
    def is_citizen(self):
        return self.user_type == self.CITIZEN
    
    def is_employee(self):
        return self.user_type == self.EMPLOYEE

class UserProfile(models.Model):
    """Extended profile information"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    photo = models.ImageField(upload_to='profiles/', blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    gender = models.CharField(
        max_length=10,
        choices=[('male', 'Male'), ('female', 'Female'), ('other', 'Other')],
        blank=True, null=True
    )
    
    # Education details
    education = models.CharField(max_length=100, blank=True, null=True)
    occupation = models.CharField(max_length=100, blank=True, null=True)
    
    # Family details
    family_members = models.IntegerField(default=1)
    ration_card_number = models.CharField(max_length=50, blank=True, null=True)
    
    # Government IDs
    pan_number = models.CharField(max_length=10, blank=True, null=True)
    voter_id = models.CharField(max_length=20, blank=True, null=True)
    driving_license = models.CharField(max_length=20, blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Profile of {self.user.username}"
    
    def get_complete_address(self):
        address_parts = []
        if self.user.address:
            address_parts.append(self.user.address)
        if self.user.district:
            address_parts.append(self.user.district)
        if self.user.pincode:
            address_parts.append(f"PIN: {self.user.pincode}")
        return ", ".join(address_parts)