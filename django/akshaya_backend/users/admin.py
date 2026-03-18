"""
Admin configuration for Users app
"""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _

from .models import User, UserProfile

class UserProfileInline(admin.StackedInline):
    """Inline admin for UserProfile"""
    model = UserProfile
    can_delete = False
    verbose_name_plural = _('Profile')

class UserAdmin(BaseUserAdmin):
    """Admin interface for User model"""
    inlines = [UserProfileInline]
    list_display = ('username', 'email', 'first_name', 'last_name', 
                   'user_type', 'district', 'is_active', 'date_joined')
    list_filter = ('user_type', 'is_active', 'is_staff', 'is_superuser', 'district')
    search_fields = ('username', 'email', 'first_name', 'last_name', 'phone', 'aadhaar_number')
    ordering = ('-date_joined',)
    
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email', 
                                        'phone', 'aadhaar_number', 'preferred_language')}),
        (_('Address'), {'fields': ('address', 'district', 'pincode')}),
        (_('Permissions'), {'fields': ('user_type', 'is_active', 'is_staff', 
                                      'is_superuser', 'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
        (_('Verification'), {'fields': ('is_phone_verified', 'is_email_verified')}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'user_type'),
        }),
    )

admin.site.register(User, UserAdmin)