"""
Serializers for Services app
"""
from rest_framework import serializers
from django.utils.translation import gettext_lazy as _

from .models import Service, ServiceCategory, ServiceStep, ServiceFAQ, ServiceApplication
from documents.models import DocumentType

class ServiceCategorySerializer(serializers.ModelSerializer):
    """Serializer for ServiceCategory"""
    service_count = serializers.IntegerField(source='services.count', read_only=True)
    
    class Meta:
        model = ServiceCategory
        fields = ['id', 'name', 'description', 'icon', 'color', 
                 'order', 'is_active', 'service_count']
        read_only_fields = ['service_count']

class ServiceStepSerializer(serializers.ModelSerializer):
    """Serializer for ServiceStep"""
    class Meta:
        model = ServiceStep
        fields = ['id', 'step_number', 'title', 'description', 
                 'estimated_time', 'is_online']

class ServiceFAQSerializer(serializers.ModelSerializer):
    """Serializer for ServiceFAQ"""
    class Meta:
        model = ServiceFAQ
        fields = ['id', 'question', 'answer', 'order']

class DocumentTypeSerializer(serializers.ModelSerializer):
    """Serializer for DocumentType (simplified)"""
    class Meta:
        model = DocumentType
        fields = ['id', 'name', 'description', 'is_mandatory', 'max_size_mb']

class ServiceSerializer(serializers.ModelSerializer):
    """Serializer for Service"""
    category = ServiceCategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=ServiceCategory.objects.all(),
        source='category',
        write_only=True
    )
    steps = ServiceStepSerializer(many=True, read_only=True)
    faqs = ServiceFAQSerializer(many=True, read_only=True)
    required_documents = DocumentTypeSerializer(many=True, read_only=True)
    application_count = serializers.IntegerField(source='applications.count', read_only=True)
    
    class Meta:
        model = Service
        fields = [
            'id', 'name', 'service_type', 'slug', 'description', 'detailed_description',
            'category', 'category_id', 'department', 'processing_time', 'fee',
            'online_available', 'offline_centers', 'icon', 'is_featured',
            'popularity', 'is_active', 'steps', 'faqs', 'required_documents',
            'application_count', 'created_at', 'updated_at'
        ]
        read_only_fields = ['slug', 'popularity', 'created_at', 'updated_at', 
                           'application_count']
    
    def create(self, validated_data):
        """Create service with slug"""
        from django.utils.text import slugify
        service = Service(**validated_data)
        if not service.slug:
            service.slug = slugify(service.name)
        
        # Ensure unique slug
        original_slug = service.slug
        counter = 1
        while Service.objects.filter(slug=service.slug).exists():
            service.slug = f"{original_slug}-{counter}"
            counter += 1
        
        service.save()
        return service

class ServiceApplicationSerializer(serializers.ModelSerializer):
    """Serializer for ServiceApplication"""
    service_name = serializers.CharField(source='service.name', read_only=True)
    user_name = serializers.CharField(source='user.get_full_name', read_only=True)
    employee_name = serializers.CharField(source='assigned_to.user.get_full_name', 
                                         read_only=True, allow_null=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    status_color = serializers.CharField(source='get_status_color', read_only=True)
    
    class Meta:
        model = ServiceApplication
        fields = [
            'id', 'reference_number', 'service', 'service_name', 'user', 'user_name',
            'status', 'status_display', 'status_color', 'form_data',
            'payment_status', 'payment_reference', 'assigned_to', 'employee_name',
            'submitted_at', 'reviewed_at', 'completed_at',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['reference_number', 'created_at', 'updated_at']
    
    def validate(self, data):
        """Validate application data"""
        user = self.context['request'].user
        service = data.get('service')
        
        # Check if service is active
        if service and not service.is_active:
            raise serializers.ValidationError(
                {"service": _("This service is currently unavailable.")}
            )
        
        # Limit draft applications per user
        if data.get('status') == ServiceApplication.DRAFT:
            draft_count = ServiceApplication.objects.filter(
                user=user, status=ServiceApplication.DRAFT
            ).count()
            if draft_count >= 10:
                raise serializers.ValidationError(
                    {"status": _("Maximum draft applications limit reached.")}
                )
        
        return data
    
    def create(self, validated_data):
        """Create application with user from context"""
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)

class ServiceSearchSerializer(serializers.Serializer):
    """Serializer for service search"""
    query = serializers.CharField(max_length=200, required=True)
    category = serializers.CharField(max_length=100, required=False)
    online_only = serializers.BooleanField(default=False)
    
    def search(self):
        """Perform search"""
        from django.db.models import Q
        query = self.validated_data['query']
        category = self.validated_data.get('category')
        online_only = self.validated_data.get('online_only', False)
        
        services = Service.objects.filter(is_active=True)
        
        # Search in multiple fields
        if query:
            services = services.filter(
                Q(name__icontains=query) |
                Q(description__icontains=query) |
                Q(detailed_description__icontains=query) |
                Q(service_type__icontains=query)
            )
        
        # Filter by category
        if category:
            services = services.filter(category__name__icontains=category)
        
        # Filter by online availability
        if online_only:
            services = services.filter(online_available=True)
        
        return services.order_by('-is_featured', '-popularity', 'name')