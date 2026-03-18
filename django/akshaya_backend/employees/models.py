"""
Employee models for Agadh platform
"""
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings

class Employee(models.Model):
    """Akshaya Center Employee"""
    
    # Designation choices
    DESIGNATION_CHOICES = [
        ('manager', 'Center Manager'),
        ('operator', 'Computer Operator'),
        ('assistant', 'Assistant'),
        ('supervisor', 'Supervisor'),
        ('coordinator', 'Coordinator'),
    ]
    
    # Department choices
    DEPARTMENT_CHOICES = [
        ('registration', 'Registration Services'),
        ('certificate', 'Certificate Services'),
        ('finance', 'Financial Services'),
        ('support', 'Customer Support'),
        ('technical', 'Technical Support'),
        ('administration', 'Administration'),
    ]
    
    # Basic information
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='employee_profile'
    )
    employee_id = models.CharField(max_length=20, unique=True)
    designation = models.CharField(max_length=20, choices=DESIGNATION_CHOICES)
    department = models.CharField(max_length=20, choices=DEPARTMENT_CHOICES)
    
    # Center information
    center = models.ForeignKey('AkshayaCenter', on_delete=models.CASCADE, related_name='employees')
    
    # Contact information
    official_email = models.EmailField(unique=True)
    official_phone = models.CharField(max_length=15)
    alternate_phone = models.CharField(max_length=15, blank=True, null=True)
    
    # Work details
    specialization = models.CharField(max_length=100, blank=True, null=True)
    experience_years = models.IntegerField(default=0)
    skills = models.TextField(blank=True, null=True, help_text="Comma-separated skills")
    
    # Availability
    is_available = models.BooleanField(default=True)
    working_hours = models.CharField(max_length=100, default="9:00 AM - 5:00 PM")
    working_days = models.CharField(max_length=100, default="Monday to Saturday")
    
    # Performance metrics
    rating = models.FloatField(default=5.0, help_text="Average rating out of 5")
    tasks_completed = models.IntegerField(default=0)
    pending_tasks = models.IntegerField(default=0)
    
    # Government details
    govt_id = models.CharField(max_length=50, blank=True, null=True)
    joining_date = models.DateField(null=True, blank=True)
    
    # Verification
    is_verified = models.BooleanField(default=False)
    verification_date = models.DateField(null=True, blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _('Employee')
        verbose_name_plural = _('Employees')
        ordering = ['-rating', 'employee_id']
    
    def __str__(self):
        return f"{self.user.get_full_name()} - {self.get_designation_display()}"
    
    def get_full_info(self):
        """Get complete employee information"""
        return {
            'id': self.id,
            'name': self.user.get_full_name(),
            'employee_id': self.employee_id,
            'designation': self.get_designation_display(),
            'department': self.get_department_display(),
            'center': self.center.name,
            'location': self.center.location,
            'email': self.official_email,
            'phone': self.official_phone,
            'availability': self.is_available,
            'rating': self.rating,
            'experience': f"{self.experience_years} years"
        }

class AkshayaCenter(models.Model):
    """Akshaya Center Information"""
    
    # Center status
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('maintenance', 'Under Maintenance'),
        ('temporary', 'Temporary Closed'),
    ]
    
    # Basic information
    center_code = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=200)
    address = models.TextField()
    location = models.CharField(max_length=100, help_text="District/Locality")
    district = models.CharField(max_length=50, default='Kozhikode')
    pincode = models.CharField(max_length=10)
    
    # Contact information
    phone = models.CharField(max_length=15)
    email = models.EmailField()
    website = models.URLField(blank=True, null=True)
    
    # Operational details
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    established_date = models.DateField(null=True, blank=True)
    working_hours = models.CharField(max_length=100, default="9:00 AM - 5:00 PM")
    working_days = models.CharField(max_length=100, default="Monday to Saturday")
    
    # Facilities
    has_wifi = models.BooleanField(default=True)
    has_printer = models.BooleanField(default=True)
    has_scanner = models.BooleanField(default=True)
    has_biometric = models.BooleanField(default=True)
    has_wheelchair_access = models.BooleanField(default=False)
    parking_available = models.BooleanField(default=False)
    
    # Services offered (many-to-many through ServiceCenter)
    services = models.ManyToManyField('services.Service', through='ServiceCenter')
    
    # Capacity
    max_capacity = models.IntegerField(default=50, help_text="Maximum daily visitors")
    current_employees = models.IntegerField(default=0)
    
    # Location coordinates (for maps)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    
    # Ratings
    average_rating = models.FloatField(default=5.0)
    total_ratings = models.IntegerField(default=0)
    
    # Government details
    govt_code = models.CharField(max_length=50, blank=True, null=True)
    nodal_officer = models.CharField(max_length=100, blank=True, null=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _('Akshaya Center')
        verbose_name_plural = _('Akshaya Centers')
        ordering = ['district', 'name']
    
    def __str__(self):
        return f"{self.name} - {self.location}"
    
    def get_full_address(self):
        """Get complete address"""
        return f"{self.address}, {self.location}, {self.district} - {self.pincode}"
    
    def get_employee_count(self):
        """Get number of active employees"""
        return self.employees.filter(user__is_active=True).count()
    
    def update_employee_count(self):
        """Update employee count"""
        self.current_employees = self.get_employee_count()
        self.save()

class ServiceCenter(models.Model):
    """Link between Service and AkshayaCenter"""
    service = models.ForeignKey('services.Service', on_delete=models.CASCADE)
    center = models.ForeignKey(AkshayaCenter, on_delete=models.CASCADE)
    is_available = models.BooleanField(default=True)
    fee_at_center = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    processing_days = models.IntegerField(default=7, help_text="Processing days at this center")
    special_notes = models.TextField(blank=True, null=True)
    
    class Meta:
        unique_together = ['service', 'center']
        verbose_name = _('Service at Center')
        verbose_name_plural = _('Services at Centers')
    
    def __str__(self):
        return f"{self.service.name} at {self.center.name}"

class EmployeeAvailability(models.Model):
    """Track employee availability"""
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='availabilities')
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    is_available = models.BooleanField(default=True)
    reason = models.CharField(max_length=200, blank=True, null=True, 
                             help_text="Reason for unavailability")
    
    class Meta:
        unique_together = ['employee', 'date']
        verbose_name = _('Employee Availability')
        verbose_name_plural = _('Employee Availabilities')
        ordering = ['date', 'start_time']
    
    def __str__(self):
        status = "Available" if self.is_available else "Unavailable"
        return f"{self.employee.user.get_full_name()} - {self.date} ({status})"

class EmployeeRating(models.Model):
    """Employee ratings by users"""
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='ratings')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, 
                           related_name='given_ratings')
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    feedback = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['employee', 'user']
        verbose_name = _('Employee Rating')
        verbose_name_plural = _('Employee Ratings')
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.employee.user.get_full_name()} - {self.rating}/5"
    
    def save(self, *args, **kwargs):
        """Update employee's average rating"""
        super().save(*args, **kwargs)
        self.employee.update_average_rating()

class TaskAssignment(models.Model):
    """Task assignments to employees"""
    
    # Task status
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    
    # Priority levels
    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('urgent', 'Urgent'),
    ]
    
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='tasks')
    application = models.ForeignKey('services.ServiceApplication', on_delete=models.CASCADE, 
                                   related_name='task_assignments')
    assigned_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
                                   null=True, related_name='assigned_tasks')
    
    task_description = models.TextField()
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='medium')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    
    deadline = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    
    notes = models.TextField(blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _('Task Assignment')
        verbose_name_plural = _('Task Assignments')
        ordering = ['-priority', 'deadline']
    
    def __str__(self):
        return f"Task for {self.employee.user.get_full_name()} - {self.status}"
    
    def save(self, *args, **kwargs):
        """Update employee task counts"""
        is_new = self.pk is None
        old_status = None
        
        if not is_new:
            old_task = TaskAssignment.objects.get(pk=self.pk)
            old_status = old_task.status
        
        super().save(*args, **kwargs)
        
        # Update employee task counts
        if is_new or old_status != self.status:
            self.employee.update_task_counts()