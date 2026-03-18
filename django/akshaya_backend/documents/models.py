"""
Document models for Agadh platform
"""
import os
import uuid
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from django.core.validators import FileExtensionValidator

def document_upload_path(instance, filename):
    """Generate upload path for documents"""
    ext = filename.split('.')[-1]
    filename = f"{uuid.uuid4()}.{ext}"
    return f'documents/{instance.document_type.service.slug}/{filename}'

class DocumentType(models.Model):
    """Type of document required for services"""
    
    # Document categories
    CATEGORY_CHOICES = [
        ('identity', 'Identity Proof'),
        ('address', 'Address Proof'),
        ('income', 'Income Proof'),
        ('education', 'Education Proof'),
        ('family', 'Family Proof'),
        ('property', 'Property Proof'),
        ('medical', 'Medical Certificate'),
        ('other', 'Other Documents'),
    ]
    
    # Service reference
    service = models.ForeignKey(
        'services.Service',
        on_delete=models.CASCADE,
        related_name='required_documents'
    )
    
    # Basic information
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='other')
    
    # Requirements
    is_mandatory = models.BooleanField(default=True)
    max_size_mb = models.IntegerField(default=5, help_text="Maximum file size in MB")
    allowed_extensions = models.CharField(
        max_length=100,
        default='pdf,jpg,jpeg,png',
        help_text="Comma-separated file extensions (e.g., pdf,jpg,png)"
    )
    
    # Examples and templates
    example_url = models.URLField(blank=True, null=True, help_text="URL to example document")
    template_file = models.FileField(
        upload_to='document_templates/',
        blank=True, null=True,
        help_text="Template file for this document"
    )
    
    # Validity information
    validity_days = models.IntegerField(
        default=0,
        help_text="Validity period in days (0 for no expiry)"
    )
    
    # Verification
    requires_verification = models.BooleanField(default=False)
    verification_instructions = models.TextField(blank=True, null=True)
    
    # Metadata
    order = models.IntegerField(default=0, help_text="Display order")
    is_active = models.BooleanField(default=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _('Document Type')
        verbose_name_plural = _('Document Types')
        ordering = ['service', 'order', 'name']
        unique_together = ['service', 'name']
    
    def __str__(self):
        return f"{self.name} - {self.service.name}"
    
    def get_allowed_extensions_list(self):
        """Get list of allowed extensions"""
        return [ext.strip().lower() for ext in self.allowed_extensions.split(',')]
    
    def is_extension_allowed(self, filename):
        """Check if file extension is allowed"""
        ext = filename.split('.')[-1].lower()
        return ext in self.get_allowed_extensions_list()

class UserDocument(models.Model):
    """Documents uploaded by users"""
    
    # Document status
    STATUS_CHOICES = [
        ('uploaded', 'Uploaded'),
        ('verifying', 'Under Verification'),
        ('verified', 'Verified'),
        ('rejected', 'Rejected'),
        ('expired', 'Expired'),
    ]
    
    # Basic information
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='documents'
    )
    document_type = models.ForeignKey(
        DocumentType,
        on_delete=models.CASCADE,
        related_name='user_documents'
    )
    
    # File storage
    file = models.FileField(
        upload_to=document_upload_path,
        validators=[
            FileExtensionValidator(allowed_extensions=['pdf', 'jpg', 'jpeg', 'png'])
        ]
    )
    original_filename = models.CharField(max_length=255)
    file_size = models.IntegerField(help_text="File size in bytes")
    file_hash = models.CharField(max_length=64, blank=True, help_text="SHA256 hash for verification")
    
    # Document details
    document_number = models.CharField(max_length=100, blank=True, null=True)
    issue_date = models.DateField(null=True, blank=True)
    expiry_date = models.DateField(null=True, blank=True)
    issuing_authority = models.CharField(max_length=200, blank=True, null=True)
    
    # Status and verification
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='uploaded')
    verified_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='verified_documents'
    )
    verification_date = models.DateTimeField(null=True, blank=True)
    rejection_reason = models.TextField(blank=True, null=True)
    
    # Metadata
    is_primary = models.BooleanField(default=False, help_text="Primary document for this type")
    metadata = models.JSONField(default=dict, blank=True, help_text="Additional metadata")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _('User Document')
        verbose_name_plural = _('User Documents')
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', 'document_type', 'status']),
            models.Index(fields=['status', 'expiry_date']),
        ]
    
    def __str__(self):
        return f"{self.document_type.name} - {self.user.get_full_name()}"
    
    def save(self, *args, **kwargs):
        """Calculate file hash and size before saving"""
        if self.file and not self.file_hash:
            # Calculate file hash (simplified for example)
            import hashlib
            self.file.seek(0)
            file_content = self.file.read()
            self.file_hash = hashlib.sha256(file_content).hexdigest()
            self.file_size = len(file_content)
        
        # Set expiry date if validity period is specified
        if not self.expiry_date and self.document_type.validity_days > 0 and self.issue_date:
            from datetime import timedelta
            self.expiry_date = self.issue_date + timedelta(days=self.document_type.validity_days)
        
        super().save(*args, **kwargs)
    
    def is_expired(self):
        """Check if document is expired"""
        from django.utils import timezone
        if self.expiry_date:
            return self.expiry_date < timezone.now().date()
        return False
    
    def get_file_url(self):
        """Get file URL if file exists"""
        if self.file and hasattr(self.file, 'url'):
            return self.file.url
        return None
    
    def get_file_size_mb(self):
        """Get file size in MB"""
        return round(self.file_size / (1024 * 1024), 2)

class SubmittedDocument(models.Model):
    """Documents submitted with service applications"""
    
    application = models.ForeignKey(
        'services.ServiceApplication',
        on_delete=models.CASCADE,
        related_name='submitted_documents'
    )
    document_type = models.ForeignKey(
        DocumentType,
        on_delete=models.CASCADE,
        related_name='submissions'
    )
    user_document = models.ForeignKey(
        UserDocument,
        on_delete=models.CASCADE,
        related_name='submissions',
        null=True, blank=True
    )
    
    # If uploaded directly with application
    file = models.FileField(
        upload_to='application_documents/',
        null=True, blank=True
    )
    
    # Status
    is_verified = models.BooleanField(default=False)
    verification_notes = models.TextField(blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _('Submitted Document')
        verbose_name_plural = _('Submitted Documents')
        unique_together = ['application', 'document_type']
    
    def __str__(self):
        return f"{self.document_type.name} for {self.application.reference_number}"
    
    def get_document_url(self):
        """Get document URL"""
        if self.user_document:
            return self.user_document.get_file_url()
        elif self.file:
            return self.file.url
        return None

class DocumentVerificationLog(models.Model):
    """Log of document verification activities"""
    
    VERIFICATION_TYPES = [
        ('auto', 'Automatic'),
        ('manual', 'Manual'),
        ('system', 'System'),
    ]
    
    document = models.ForeignKey(
        UserDocument,
        on_delete=models.CASCADE,
        related_name='verification_logs'
    )
    verified_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='document_verifications'
    )
    
    old_status = models.CharField(max_length=20)
    new_status = models.CharField(max_length=20)
    verification_type = models.CharField(max_length=20, choices=VERIFICATION_TYPES, default='manual')
    
    notes = models.TextField(blank=True, null=True)
    metadata = models.JSONField(default=dict, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = _('Document Verification Log')
        verbose_name_plural = _('Document Verification Logs')
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Verification: {self.document} - {self.old_status} to {self.new_status}"

class DocumentTemplate(models.Model):
    """Templates for document generation"""
    
    TEMPLATE_TYPES = [
        ('application', 'Application Form'),
        ('certificate', 'Certificate'),
        ('letter', 'Official Letter'),
        ('receipt', 'Receipt'),
        ('other', 'Other'),
    ]
    
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    template_type = models.CharField(max_length=20, choices=TEMPLATE_TYPES, default='application')
    
    # Template file
    template_file = models.FileField(upload_to='document_templates/')
    
    # Associated services
    services = models.ManyToManyField(
        'services.Service',
        related_name='templates',
        blank=True
    )
    
    # Template variables
    variables = models.JSONField(
        default=list,
        help_text="List of variable names used in template"
    )
    
    # Metadata
    is_active = models.BooleanField(default=True)
    version = models.CharField(max_length=20, default='1.0')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _('Document Template')
        verbose_name_plural = _('Document Templates')
        ordering = ['name']
    
    def __str__(self):
        return f"{self.name} v{self.version}"
    
    def get_variables_list(self):
        """Get list of template variables"""
        return self.variables if isinstance(self.variables, list) else []