"""
Serializers for Employees app
"""
from rest_framework import serializers
from django.utils.translation import gettext_lazy as _

from .models import (
    Employee, AkshayaCenter, ServiceCenter,
    EmployeeAvailability, EmployeeRating, TaskAssignment
)
from users.serializers import UserSerializer

class AkshayaCenterSerializer(serializers.ModelSerializer):
    """Serializer for AkshayaCenter"""
    employee_count = serializers.IntegerField(source='get_employee_count', read_only=True)
    full_address = serializers.CharField(source='get_full_address', read_only=True)
    
    class Meta:
        model = AkshayaCenter
        fields = [
            'id', 'center_code', 'name', 'address', 'location', 'district',
            'pincode', 'phone', 'email', 'website', 'status', 'established_date',
            'working_hours', 'working_days', 'has_wifi', 'has_printer',
            'has_scanner', 'has_biometric', 'has_wheelchair_access',
            'parking_available', 'max_capacity', 'current_employees',
            'employee_count', 'latitude', 'longitude', 'average_rating',
            'total_ratings', 'govt_code', 'nodal_officer', 'full_address',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['current_employees', 'average_rating', 'total_ratings']

class ServiceCenterSerializer(serializers.ModelSerializer):
    """Serializer for ServiceCenter"""
    service_name = serializers.CharField(source='service.name', read_only=True)
    center_name = serializers.CharField(source='center.name', read_only=True)
    
    class Meta:
        model = ServiceCenter
        fields = [
            'id', 'service', 'service_name', 'center', 'center_name',
            'is_available', 'fee_at_center', 'processing_days',
            'special_notes'
        ]

class EmployeeSerializer(serializers.ModelSerializer):
    """Serializer for Employee"""
    user = UserSerializer(read_only=True)
    center_info = AkshayaCenterSerializer(source='center', read_only=True)
    designation_display = serializers.CharField(source='get_designation_display', read_only=True)
    department_display = serializers.CharField(source='get_department_display', read_only=True)
    
    class Meta:
        model = Employee
        fields = [
            'id', 'user', 'employee_id', 'designation', 'designation_display',
            'department', 'department_display', 'center', 'center_info',
            'official_email', 'official_phone', 'alternate_phone',
            'specialization', 'experience_years', 'skills',
            'is_available', 'working_hours', 'working_days',
            'rating', 'tasks_completed', 'pending_tasks',
            'govt_id', 'joining_date', 'is_verified', 'verification_date',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['rating', 'tasks_completed', 'pending_tasks', 'is_verified']

class EmployeeAvailabilitySerializer(serializers.ModelSerializer):
    """Serializer for EmployeeAvailability"""
    employee_name = serializers.CharField(source='employee.user.get_full_name', read_only=True)
    
    class Meta:
        model = EmployeeAvailability
        fields = [
            'id', 'employee', 'employee_name', 'date', 'start_time',
            'end_time', 'is_available', 'reason'
        ]
    
    def validate(self, data):
        """Validate availability data"""
        if data['start_time'] >= data['end_time']:
            raise serializers.ValidationError(
                {"end_time": _("End time must be after start time.")}
            )
        
        # Check for overlapping availabilities
        if self.instance:
            overlapping = EmployeeAvailability.objects.filter(
                employee=data.get('employee', self.instance.employee),
                date=data.get('date', self.instance.date),
                start_time__lt=data.get('end_time', self.instance.end_time),
                end_time__gt=data.get('start_time', self.instance.start_time)
            ).exclude(pk=self.instance.pk)
        else:
            overlapping = EmployeeAvailability.objects.filter(
                employee=data['employee'],
                date=data['date'],
                start_time__lt=data['end_time'],
                end_time__gt=data['start_time']
            )
        
        if overlapping.exists():
            raise serializers.ValidationError(
                _("This time slot overlaps with existing availability.")
            )
        
        return data

class EmployeeRatingSerializer(serializers.ModelSerializer):
    """Serializer for EmployeeRating"""
    employee_name = serializers.CharField(source='employee.user.get_full_name', read_only=True)
    user_name = serializers.CharField(source='user.get_full_name', read_only=True)
    
    class Meta:
        model = EmployeeRating
        fields = [
            'id', 'employee', 'employee_name', 'user', 'user_name',
            'rating', 'feedback', 'created_at'
        ]
        read_only_fields = ['user', 'created_at']
    
    def validate(self, data):
        """Validate rating data"""
        # Ensure user can't rate themselves
        request = self.context.get('request')
        if request and request.user == data.get('employee', self.instance.employee).user:
            raise serializers.ValidationError(
                {"employee": _("You cannot rate yourself.")}
            )
        
        # Check if user has already rated this employee
        if not self.instance:  # Only for new ratings
            existing = EmployeeRating.objects.filter(
                employee=data['employee'],
                user=request.user
            ).exists()
            
            if existing:
                raise serializers.ValidationError(
                    {"employee": _("You have already rated this employee.")}
                )
        
        return data
    
    def create(self, validated_data):
        """Create rating with user from context"""
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)

class TaskAssignmentSerializer(serializers.ModelSerializer):
    """Serializer for TaskAssignment"""
    employee_name = serializers.CharField(source='employee.user.get_full_name', read_only=True)
    assigned_by_name = serializers.CharField(source='assigned_by.get_full_name', read_only=True)
    application_ref = serializers.CharField(source='application.reference_number', read_only=True)
    priority_display = serializers.CharField(source='get_priority_display', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    
    class Meta:
        model = TaskAssignment
        fields = [
            'id', 'employee', 'employee_name', 'application', 'application_ref',
            'assigned_by', 'assigned_by_name', 'task_description', 'priority',
            'priority_display', 'status', 'status_display', 'deadline',
            'completed_at', 'notes', 'created_at', 'updated_at'
        ]
        read_only_fields = ['assigned_by', 'completed_at', 'created_at', 'updated_at']
    
    def validate(self, data):
        """Validate task assignment"""
        # Check if employee is available
        employee = data.get('employee', self.instance.employee if self.instance else None)
        if employee and not employee.is_available:
            raise serializers.ValidationError(
                {"employee": _("Selected employee is not available.")}
            )
        
        # Check deadline
        deadline = data.get('deadline')
        if deadline and deadline <= data.get('created_at'):
            raise serializers.ValidationError(
                {"deadline": _("Deadline must be in the future.")}
            )
        
        return data
    
    def create(self, validated_data):
        """Create task with assigned_by from context"""
        validated_data['assigned_by'] = self.context['request'].user
        return super().create(validated_data)

class EmployeeSearchSerializer(serializers.Serializer):
    """Serializer for employee search"""
    query = serializers.CharField(max_length=200, required=False)
    designation = serializers.CharField(max_length=20, required=False)
    department = serializers.CharField(max_length=20, required=False)
    center = serializers.IntegerField(required=False)
    available_only = serializers.BooleanField(default=False)
    
    def search(self):
        """Perform search"""
        from django.db.models import Q
        
        employees = Employee.objects.select_related('user', 'center').filter(
            user__is_active=True
        )
        
        query = self.validated_data.get('query')
        if query:
            employees = employees.filter(
                Q(user__first_name__icontains=query) |
                Q(user__last_name__icontains=query) |
                Q(employee_id__icontains=query) |
                Q(specialization__icontains=query) |
                Q(skills__icontains=query)
            )
        
        designation = self.validated_data.get('designation')
        if designation:
            employees = employees.filter(designation=designation)
        
        department = self.validated_data.get('department')
        if department:
            employees = employees.filter(department=department)
        
        center = self.validated_data.get('center')
        if center:
            employees = employees.filter(center_id=center)
        
        available_only = self.validated_data.get('available_only', False)
        if available_only:
            employees = employees.filter(is_available=True)
        
        return employees.order_by('-rating', 'user__first_name')

class CenterSearchSerializer(serializers.Serializer):
    """Serializer for center search"""
    query = serializers.CharField(max_length=200, required=False)
    district = serializers.CharField(max_length=50, required=False)
    service = serializers.IntegerField(required=False)
    has_facility = serializers.CharField(max_length=50, required=False)
    
    def search(self):
        """Perform search"""
        from django.db.models import Q
        
        centers = AkshayaCenter.objects.filter(status='active')
        
        query = self.validated_data.get('query')
        if query:
            centers = centers.filter(
                Q(name__icontains=query) |
                Q(location__icontains=query) |
                Q(address__icontains=query)
            )
        
        district = self.validated_data.get('district')
        if district:
            centers = centers.filter(district__icontains=district)
        
        service = self.validated_data.get('service')
        if service:
            centers = centers.filter(services__id=service)
        
        has_facility = self.validated_data.get('has_facility')
        if has_facility:
            if has_facility == 'wifi':
                centers = centers.filter(has_wifi=True)
            elif has_facility == 'printer':
                centers = centers.filter(has_printer=True)
            elif has_facility == 'wheelchair':
                centers = centers.filter(has_wheelchair_access=True)
            elif has_facility == 'parking':
                centers = centers.filter(parking_available=True)
        
        return centers.order_by('district', 'name')