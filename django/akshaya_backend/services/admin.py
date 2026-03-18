"""
Admin configuration for Services app
"""
from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from .models import Service, ServiceCategory, ServiceStep, ServiceFAQ, ServiceApplication

class ServiceStepInline(admin.TabularInline):
    """Inline admin for ServiceStep"""
    model = ServiceStep
    extra = 1
    ordering = ['step_number']

class ServiceFAQInline(admin.TabularInline):
    """Inline admin for ServiceFAQ"""
    model = ServiceFAQ
    extra = 1
    ordering = ['order']

class ServiceApplicationInline(admin.TabularInline):
    """Inline admin for ServiceApplication"""
    model = ServiceApplication
    extra = 0
    readonly_fields = ['reference_number', 'created_at']
    can_delete = False

@admin.register(ServiceCategory)
class ServiceCategoryAdmin(admin.ModelAdmin):
    """Admin for ServiceCategory"""
    list_display = ['name', 'order', 'is_active', 'service_count']
    list_editable = ['order', 'is_active']
    list_filter = ['is_active']
    search_fields = ['name']
    prepopulated_fields = {}
    
    def service_count(self, obj):
        return obj.services.count()
    service_count.short_description = _('Services')

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    """Admin for Service"""
    list_display = ['name', 'service_type', 'category', 'fee', 
                   'online_available', 'is_featured', 'is_active', 'popularity']
    list_filter = ['service_type', 'category', 'is_active', 'is_featured', 'online_available']
    search_fields = ['name', 'description', 'department']
    list_editable = ['is_featured', 'is_active', 'online_available']
    prepopulated_fields = {'slug': ('name',)}
    inlines = [ServiceStepInline, ServiceFAQInline]
    
    fieldsets = (
        (None, {
            'fields': ('name', 'slug', 'service_type', 'category', 'description', 
                      'detailed_description')
        }),
        (_('Service Details'), {
            'fields': ('department', 'processing_time', 'fee', 'online_available', 
                      'offline_centers')
        }),
        (_('Presentation'), {
            'fields': ('icon', 'is_featured')
        }),
        (_('Metadata'), {
            'fields': ('popularity', 'is_active')
        }),
    )

@admin.register(ServiceApplication)
class ServiceApplicationAdmin(admin.ModelAdmin):
    """Admin for ServiceApplication"""
    list_display = ['reference_number', 'service', 'user', 'status', 
                   'payment_status', 'created_at', 'submitted_at']
    list_filter = ['status', 'payment_status', 'service', 'created_at']
    search_fields = ['reference_number', 'user__username', 'user__email']
    readonly_fields = ['reference_number', 'created_at', 'updated_at']
    date_hierarchy = 'created_at'
    
    fieldsets = (
        (None, {
            'fields': ('reference_number', 'service', 'user', 'status')
        }),
        (_('Application Data'), {
            'fields': ('form_data',)
        }),
        (_('Payment'), {
            'fields': ('payment_status', 'payment_reference')
        }),
        (_('Assignment'), {
            'fields': ('assigned_to',)
        }),
        (_('Timestamps'), {
            'fields': ('submitted_at', 'reviewed_at', 'completed_at', 
                      'created_at', 'updated_at')
        }),
    )
    
    def get_readonly_fields(self, request, obj=None):
        """Make certain fields read-only after submission"""
        readonly_fields = list(self.readonly_fields)
        if obj and obj.status != ServiceApplication.DRAFT:
            readonly_fields.extend(['service', 'user', 'form_data'])
        return readonly_fields

# Register remaining models
admin.site.register(ServiceStep)
admin.site.register(ServiceFAQ)