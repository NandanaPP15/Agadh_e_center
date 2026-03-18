"""
Service models for Agadh platform
"""
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator, MaxValueValidator

class ServiceCategory(models.Model):
    """Category for grouping services"""
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=50, blank=True, help_text="FontAwesome icon class")
    color = models.CharField(max_length=20, default='#4CAF50', help_text="Hex color code")
    order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = _('Service Category')
        verbose_name_plural = _('Service Categories')
        ordering = ['order', 'name']
    
    def __str__(self):
        return self.name

class Service(models.Model):
    """Government service model"""
    # Service types
    RATION_CARD = 'ration_card'
    MARRIAGE_REGISTRATION = 'marriage_registration'
    POLICE_CLEARANCE = 'police_clearance'
    PAN_CARD = 'pan_card'
    BIRTH_CERTIFICATE = 'birth_certificate'
    PASSPORT = 'passport'
    AADHAAR = 'aadhaar'
    DEATH_REGISTRATION = 'death_registration'
    NCL_CERTIFICATE = 'ncl_certificate'
    
    SERVICE_TYPE_CHOICES = [
        (RATION_CARD, 'Ration Card Services'),
        (MARRIAGE_REGISTRATION, 'Marriage Registration'),
        (POLICE_CLEARANCE, 'Police Clearance Certificate'),
        (PAN_CARD, 'PAN Card Services'),
        (BIRTH_CERTIFICATE, 'Birth Certificate Services'),
        (PASSPORT, 'Passport Services'),
        (AADHAAR, 'Aadhaar Services'),
        (DEATH_REGISTRATION, 'Death Registration Services'),
        (NCL_CERTIFICATE, 'Non-Creamy Layer Certificate'),
    ]
    
    # Basic info
    name = models.CharField(max_length=200)
    service_type = models.CharField(max_length=50, choices=SERVICE_TYPE_CHOICES)
    category = models.ForeignKey(ServiceCategory, on_delete=models.SET_NULL, 
                                null=True, related_name='services')
    description = models.TextField()
    detailed_description = models.TextField(blank=True)
    
    # Service details
    department = models.CharField(max_length=100)
    processing_time = models.CharField(max_length=50, help_text="e.g., 7-10 working days")
    fee = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    online_available = models.BooleanField(default=True)
    offline_centers = models.TextField(help_text="Available Akshaya centers", blank=True)
    
    # Metadata
    slug = models.SlugField(max_length=200, unique=True)
    icon = models.CharField(max_length=50, blank=True)
    is_featured = models.BooleanField(default=False)
    popularity = models.IntegerField(default=0, help_text="Number of views/applications")
    is_active = models.BooleanField(default=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _('Service')
        verbose_name_plural = _('Services')
        ordering = ['-is_featured', 'name']
        indexes = [
            models.Index(fields=['service_type', 'is_active']),
            models.Index(fields=['slug']),
        ]
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return f"/services/{self.slug}/"
    
    def increment_popularity(self):
        """Increment service popularity"""
        self.popularity += 1
        self.save(update_fields=['popularity'])

class ServiceStep(models.Model):
    """Step-by-step process for a service"""
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='steps')
    step_number = models.IntegerField()
    title = models.CharField(max_length=200)
    description = models.TextField()
    estimated_time = models.CharField(max_length=50, blank=True)
    is_online = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['service', 'step_number']
        unique_together = ['service', 'step_number']
    
    def __str__(self):
        return f"{self.service.name} - Step {self.step_number}"

class ServiceFAQ(models.Model):
    """Frequently Asked Questions for services"""
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='faqs')
    question = models.TextField()
    answer = models.TextField()
    order = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['order', 'id']
        verbose_name = 'FAQ'
        verbose_name_plural = 'FAQs'
    
    def __str__(self):
        return f"FAQ: {self.question[:50]}..."

class ServiceApplication(models.Model):
    """Track service applications"""
    # Application status
    DRAFT = 'draft'
    SUBMITTED = 'submitted'
    UNDER_REVIEW = 'under_review'
    APPROVED = 'approved'
    REJECTED = 'rejected'
    COMPLETED = 'completed'
    CANCELLED = 'cancelled'
    
    STATUS_CHOICES = [
        (DRAFT, 'Draft'),
        (SUBMITTED, 'Submitted'),
        (UNDER_REVIEW, 'Under Review'),
        (APPROVED, 'Approved'),
        (REJECTED, 'Rejected'),
        (COMPLETED, 'Completed'),
        (CANCELLED, 'Cancelled'),
    ]
    
    # Application fields
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='applications')
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='applications')
    reference_number = models.CharField(max_length=50, unique=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=DRAFT)
    
    # Application data (store as JSON for flexibility)
    form_data = models.JSONField(default=dict)
    
    # Document tracking
    documents_submitted = models.ManyToManyField('documents.DocumentType', through='documents.SubmittedDocument')
    
    # Payment tracking
    payment_status = models.CharField(max_length=20, default='pending')
    payment_reference = models.CharField(max_length=100, blank=True)
    
    # Employee assignment
    assigned_to = models.ForeignKey('employees.Employee', on_delete=models.SET_NULL, 
                                   null=True, blank=True, related_name='assigned_applications')
    
    # Timestamps
    submitted_at = models.DateTimeField(null=True, blank=True)
    reviewed_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['reference_number']),
            models.Index(fields=['status', 'created_at']),
        ]
    
    def __str__(self):
        return f"{self.reference_number} - {self.service.name}"
    
    def save(self, *args, **kwargs):
        """Generate reference number on save"""
        if not self.reference_number:
            import random
            import string
            prefix = f"AG{self.service.service_type[:3].upper()}"
            random_str = ''.join(random.choices(string.digits, k=8))
            self.reference_number = f"{prefix}{random_str}"
        
        # Update timestamps based on status
        if self.status == self.SUBMITTED and not self.submitted_at:
            self.submitted_at = models.DateTimeField(auto_now_add=True)
        elif self.status == self.COMPLETED and not self.completed_at:
            self.completed_at = models.DateTimeField(auto_now_add=True)
        
        super().save(*args, **kwargs)
    
    def get_status_color(self):
        """Get color for status"""
        colors = {
            self.DRAFT: 'secondary',
            self.SUBMITTED: 'info',
            self.UNDER_REVIEW: 'warning',
            self.APPROVED: 'success',
            self.REJECTED: 'danger',
            self.COMPLETED: 'success',
            self.CANCELLED: 'dark',
        }
        return colors.get(self.status, 'secondary')