"""
Admin configuration for Employees app
"""
from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from .models import (
    Employee, AkshayaCenter, ServiceCenter,
    EmployeeAvailability, EmployeeRating, TaskAssignment
)

@admin.register(AkshayaCenter)
class AkshayaCenterAdmin(admin.ModelAdmin):
    """Admin for AkshayaCenter"""
    list_display = ['name', 'center_code', 'district', 'location',
                   'status', 'current_employees', 'average_rating']
    list_filter = ['status', 'district', 'has_wifi', 'has_wheelchair_access']
    search_fields = ['name', 'center_code', 'location', 'address']
    list_editable = ['status']
    
    fieldsets = (
        (None, {
            'fields': ('center_code', 'name', 'address', 'location', 'district',
                      'pincode', 'phone', 'email', 'website')
        }),
        (_('Operational Details'), {
            'fields': ('status', 'established_date', 'working_hours',
                      'working_days', 'max_capacity')
        }),
        (_('Facilities'), {
            'fields': ('has_wifi', 'has_printer', 'has_scanner', 'has_biometric',
                      'has_wheelchair_access', 'parking_available')
        }),
        (_('Location'), {
            'fields': ('latitude', 'longitude')
        }),
        (_('Ratings'), {
            'fields': ('average_rating', 'total_ratings')
        }),
        (_('Government Details'), {
            'fields': ('govt_code', 'nodal_officer')
        }),
    )

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    """Admin for Employee"""
    list_display = ['user', 'employee_id', 'designation', 'department',
                   'center', 'is_available', 'rating', 'is_verified']
    list_filter = ['designation', 'department', 'center', 'is_available',
                  'is_verified']
    search_fields = ['user__username', 'user__first_name', 'user__last_name',
                    'employee_id', 'official_email']
    list_editable = ['is_available', 'is_verified']
    
    fieldsets = (
        (None, {
            'fields': ('user', 'employee_id', 'designation', 'department',
                      'center')
        }),
        (_('Contact Information'), {
            'fields': ('official_email', 'official_phone', 'alternate_phone')
        }),
        (_('Professional Details'), {
            'fields': ('specialization', 'experience_years', 'skills',
                      'working_hours', 'working_days')
        }),
        (_('Availability'), {
            'fields': ('is_available',)
        }),
        (_('Performance'), {
            'fields': ('rating', 'tasks_completed', 'pending_tasks')
        }),
        (_('Government Details'), {
            'fields': ('govt_id', 'joining_date')
        }),
        (_('Verification'), {
            'fields': ('is_verified', 'verification_date')
        }),
    )

@admin.register(ServiceCenter)
class ServiceCenterAdmin(admin.ModelAdmin):
    """Admin for ServiceCenter"""
    list_display = ['service', 'center', 'is_available', 'fee_at_center',
                   'processing_days']
    list_filter = ['is_available', 'center']
    search_fields = ['service__name', 'center__name']

@admin.register(EmployeeAvailability)
class EmployeeAvailabilityAdmin(admin.ModelAdmin):
    """Admin for EmployeeAvailability"""
    list_display = ['employee', 'date', 'start_time', 'end_time',
                   'is_available', 'reason']
    list_filter = ['is_available', 'date', 'employee']
    search_fields = ['employee__user__username', 'reason']

@admin.register(EmployeeRating)
class EmployeeRatingAdmin(admin.ModelAdmin):
    """Admin for EmployeeRating"""
    list_display = ['employee', 'user', 'rating', 'created_at']
    list_filter = ['rating', 'created_at']
    search_fields = ['employee__user__username', 'user__username', 'feedback']
    readonly_fields = ['created_at']

@admin.register(TaskAssignment)
class TaskAssignmentAdmin(admin.ModelAdmin):
    """Admin for TaskAssignment"""
    list_display = ['employee', 'application', 'priority', 'status',
                   'deadline', 'created_at']
    list_filter = ['priority', 'status', 'created_at']
    search_fields = ['employee__user__username', 'application__reference_number',
                    'task_description']
    readonly_fields = ['created_at', 'updated_at']