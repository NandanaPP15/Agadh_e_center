"""
Serializers for Documents app
"""
from rest_framework import serializers
from django.utils.translation import gettext_lazy as _
from django.core.validators import FileExtensionValidator

from .models import (
    DocumentType, UserDocument, SubmittedDocument,
    DocumentVerificationLog, DocumentTemplate
)
from services.serializers import ServiceSerializer

class DocumentTypeSerializer(serializers.ModelSerializer):
    """Serializer for DocumentType"""
    service_name = serializers.CharField(source='service.name', read_only=True)
    service_slug = serializers.CharField(source='service.slug', read_only=True)
    category_display = serializers.CharField(source='get_category_display', read_only=True)
    
    class Meta:
        model = DocumentType
        fields = [
            'id', 'service', 'service_name', 'service_slug', 'name',
            'description', 'category', 'category_display', 'is_mandatory',
            'max_size_mb', 'allowed_extensions', 'example_url',
            'template_file', 'validity_days', 'requires_verification',
            'verification_instructions', 'order', 'is_active',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']
    
    def validate_allowed_extensions(self, value):
        """Validate allowed extensions"""
        extensions = [ext.strip().lower() for ext in value.split(',')]
        
        # Check for valid extensions
        valid_extensions = {'pdf', 'jpg', 'jpeg', 'png', 'doc', 'docx'}
        for ext in extensions:
            if ext not in valid_extensions:
                raise serializers.ValidationError(
                    _("Invalid file extension: %(ext)s") % {'ext': ext}
                )
        
        return value

class UserDocumentSerializer(serializers.ModelSerializer):
    """Serializer for UserDocument"""
    document_type_name = serializers.CharField(source='document_type.name', read_only=True)
    service_name = serializers.CharField(source='document_type.service.name', read_only=True)
    user_name = serializers.CharField(source='user.get_full_name', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    file_url = serializers.SerializerMethodField()
    file_size_mb = serializers.SerializerMethodField()
    is_expired = serializers.SerializerMethodField()
    
    class Meta:
        model = UserDocument
        fields = [
            'id', 'user', 'user_name', 'document_type', 'document_type_name',
            'service_name', 'file', 'file_url', 'original_filename',
            'file_size', 'file_size_mb', 'file_hash', 'document_number',
            'issue_date', 'expiry_date', 'issuing_authority', 'status',
            'status_display', 'verified_by', 'verification_date',
            'rejection_reason', 'is_primary', 'metadata', 'is_expired',
            'created_at', 'updated_at'
        ]
        read_only_fields = [
            'file_hash', 'file_size', 'original_filename', 'verified_by',
            'verification_date', 'created_at', 'updated_at'
        ]
    
    def get_file_url(self, obj):
        """Get file URL"""
        return obj.get_file_url()
    
    def get_file_size_mb(self, obj):
        """Get file size in MB"""
        return obj.get_file_size_mb()
    
    def get_is_expired(self, obj):
        """Check if document is expired"""
        return obj.is_expired()
    
    def validate(self, data):
        """Validate document data"""
        # Check file size
        file = data.get('file')
        document_type = data.get('document_type', getattr(self.instance, 'document_type', None))
        
        if file and document_type:
            max_size_bytes = document_type.max_size_mb * 1024 * 1024
            
            if file.size > max_size_bytes:
                raise serializers.ValidationError({
                    'file': _("File size exceeds maximum allowed size of %(size)dMB") % 
                            {'size': document_type.max_size_mb}
                })
            
            # Check file extension
            if not document_type.is_extension_allowed(file.name):
                raise serializers.ValidationError({
                    'file': _("File extension not allowed. Allowed extensions: %(exts)s") % 
                            {'exts': document_type.allowed_extensions}
                })
        
        return data
    
    def create(self, validated_data):
        """Create user document with original filename"""
        file = validated_data.get('file')
        if file:
            validated_data['original_filename'] = file.name
        
        return super().create(validated_data)

class SubmittedDocumentSerializer(serializers.ModelSerializer):
    """Serializer for SubmittedDocument"""
    document_type_name = serializers.CharField(source='document_type.name', read_only=True)
    application_ref = serializers.CharField(source='application.reference_number', read_only=True)
    document_url = serializers.SerializerMethodField()
    
    class Meta:
        model = SubmittedDocument
        fields = [
            'id', 'application', 'application_ref', 'document_type',
            'document_type_name', 'user_document', 'file',
            'document_url', 'is_verified', 'verification_notes',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']
    
    def get_document_url(self, obj):
        """Get document URL"""
        return obj.get_document_url()
    
    def validate(self, data):
        """Validate submitted document"""
        # Ensure either user_document or file is provided
        if not data.get('user_document') and not data.get('file'):
            raise serializers.ValidationError(
                _("Either user_document or file must be provided.")
            )
        
        return data

class DocumentVerificationLogSerializer(serializers.ModelSerializer):
    """Serializer for DocumentVerificationLog"""
    document_info = serializers.CharField(source='document.__str__', read_only=True)
    verified_by_name = serializers.CharField(source='verified_by.get_full_name', read_only=True)
    verification_type_display = serializers.CharField(
        source='get_verification_type_display', read_only=True
    )
    
    class Meta:
        model = DocumentVerificationLog
        fields = [
            'id', 'document', 'document_info', 'verified_by', 'verified_by_name',
            'old_status', 'new_status', 'verification_type',
            'verification_type_display', 'notes', 'metadata', 'created_at'
        ]
        read_only_fields = ['created_at']

class DocumentTemplateSerializer(serializers.ModelSerializer):
    """Serializer for DocumentTemplate"""
    template_type_display = serializers.CharField(source='get_template_type_display', read_only=True)
    services_info = ServiceSerializer(source='services', many=True, read_only=True)
    
    class Meta:
        model = DocumentTemplate
        fields = [
            'id', 'name', 'description', 'template_type', 'template_type_display',
            'template_file', 'services', 'services_info', 'variables',
            'is_active', 'version', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']
    
    def get_variables_list(self, obj):
        """Get list of template variables"""
        return obj.get_variables_list()

class DocumentUploadSerializer(serializers.Serializer):
    """Serializer for document upload"""
    document_type = serializers.PrimaryKeyRelatedField(
        queryset=DocumentType.objects.filter(is_active=True)
    )
    file = serializers.FileField(
        validators=[
            FileExtensionValidator(allowed_extensions=['pdf', 'jpg', 'jpeg', 'png'])
        ]
    )
    document_number = serializers.CharField(required=False, allow_blank=True)
    issue_date = serializers.DateField(required=False, allow_null=True)
    expiry_date = serializers.DateField(required=False, allow_null=True)
    issuing_authority = serializers.CharField(required=False, allow_blank=True)
    is_primary = serializers.BooleanField(default=False)
    
    def validate(self, data):
        """Validate upload data"""
        document_type = data['document_type']
        file = data['file']
        
        # Check file size
        max_size_bytes = document_type.max_size_mb * 1024 * 1024
        if file.size > max_size_bytes:
            raise serializers.ValidationError({
                'file': _("File size exceeds maximum allowed size of %(size)dMB") % 
                        {'size': document_type.max_size_mb}
            })
        
        # Check file extension
        if not document_type.is_extension_allowed(file.name):
            raise serializers.ValidationError({
                'file': _("File extension not allowed. Allowed extensions: %(exts)s") % 
                        {'exts': document_type.allowed_extensions}
            })
        
        return data

class DocumentVerificationSerializer(serializers.Serializer):
    """Serializer for document verification"""
    status = serializers.ChoiceField(
        choices=['verified', 'rejected'],
        required=True
    )
    notes = serializers.CharField(required=False, allow_blank=True)
    
    def validate(self, data):
        """Validate verification data"""
        if data['status'] == 'rejected' and not data.get('notes'):
            raise serializers.ValidationError({
                'notes': _("Rejection reason is required when rejecting a document.")
            })
        
        return data