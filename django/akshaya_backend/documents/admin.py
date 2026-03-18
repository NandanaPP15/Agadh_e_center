"""
Admin configuration for Documents app
"""
from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from .models import (
    DocumentType, UserDocument, SubmittedDocument,
    DocumentVerificationLog, DocumentTemplate
)

@admin.register(DocumentType)
class DocumentTypeAdmin(admin.ModelAdmin):
    """Admin for DocumentType"""
    list_display = ['name', 'service', 'category', 'is_mandatory', 
                   'max_size_mb', 'order', 'is_active']
    list_filter = ['service', 'category', 'is_mandatory', 'is_active']
    search_fields = ['name', 'description', 'service__name']
    list_editable = ['order', 'is_active', 'is_mandatory']
    
    fieldsets = (
        (None, {
            'fields': ('service', 'name', 'description', 'category')
        }),
        (_('Requirements'), {
            'fields': ('is_mandatory', 'max_size_mb', 'allowed_extensions',
                      'validity_days', 'requires_verification')
        }),
        (_('Examples & Templates'), {
            'fields': ('example_url', 'template_file', 'verification_instructions')
        }),
        (_('Display'), {
            'fields': ('order',)
        }),
        (_('Status'), {
            'fields': ('is_active',)
        }),
    )

@admin.register(UserDocument)
class UserDocumentAdmin(admin.ModelAdmin):
    """Admin for UserDocument"""
    list_display = ['user', 'document_type', 'status', 'is_primary',
                   'issue_date', 'expiry_date', 'created_at']
    list_filter = ['status', 'is_primary', 'document_type', 'created_at']
    search_fields = ['user__username', 'user__email', 'document_number',
                    'original_filename', 'issuing_authority']
    readonly_fields = ['file_hash', 'file_size', 'original_filename',
                      'created_at', 'updated_at']
    date_hierarchy = 'created_at'
    
    fieldsets = (
        (None, {
            'fields': ('user', 'document_type', 'file', 'status')
        }),
        (_('Document Details'), {
            'fields': ('document_number', 'issue_date', 'expiry_date',
                      'issuing_authority')
        }),
        (_('Verification'), {
            'fields': ('verified_by', 'verification_date', 'rejection_reason')
        }),
        (_('Metadata'), {
            'fields': ('is_primary', 'metadata', 'file_hash', 'file_size',
                      'original_filename')
        }),
        (_('Timestamps'), {
            'fields': ('created_at', 'updated_at')
        }),
    )

@admin.register(SubmittedDocument)
class SubmittedDocumentAdmin(admin.ModelAdmin):
    """Admin for SubmittedDocument"""
    list_display = ['application', 'document_type', 'is_verified',
                   'created_at']
    list_filter = ['is_verified', 'document_type']
    search_fields = ['application__reference_number', 
                    'user_document__original_filename']
    readonly_fields = ['created_at', 'updated_at']

@admin.register(DocumentVerificationLog)
class DocumentVerificationLogAdmin(admin.ModelAdmin):
    """Admin for DocumentVerificationLog"""
    list_display = ['document', 'verified_by', 'old_status', 'new_status',
                   'verification_type', 'created_at']
    list_filter = ['verification_type', 'new_status', 'created_at']
    search_fields = ['document__user__username', 'verified_by__username',
                    'notes']
    readonly_fields = ['created_at']
    date_hierarchy = 'created_at'

@admin.register(DocumentTemplate)
class DocumentTemplateAdmin(admin.ModelAdmin):
    """Admin for DocumentTemplate"""
    list_display = ['name', 'template_type', 'version', 'is_active']
    list_filter = ['template_type', 'is_active']
    search_fields = ['name', 'description']
    filter_horizontal = ['services']
    
    fieldsets = (
        (None, {
            'fields': ('name', 'description', 'template_type', 'template_file')
        }),
        (_('Configuration'), {
            'fields': ('services', 'variables')
        }),
        (_('Versioning'), {
            'fields': ('version',)
        }),
        (_('Status'), {
            'fields': ('is_active',)
        }),
    )