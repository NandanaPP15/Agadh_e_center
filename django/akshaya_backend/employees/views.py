"""
Views for Employees app
"""
from rest_framework import viewsets, generics, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from django.utils.translation import gettext_lazy as _
from django.db.models import Q, Avg, Count

from .models import (
    Employee, AkshayaCenter, ServiceCenter,
    EmployeeAvailability, EmployeeRating, TaskAssignment
)
from .serializers import (
    EmployeeSerializer, AkshayaCenterSerializer, ServiceCenterSerializer,
    EmployeeAvailabilitySerializer, EmployeeRatingSerializer,
    TaskAssignmentSerializer, EmployeeSearchSerializer,
    CenterSearchSerializer
)

class AkshayaCenterViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for AkshayaCenter"""
    queryset = AkshayaCenter.objects.filter(status='active').annotate(
        employee_count=Count('employees', filter=Q(employees__user__is_active=True))
    ).order_by('district', 'name')
    serializer_class = AkshayaCenterSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['district', 'status']
    search_fields = ['name', 'location', 'address', 'center_code']
    
    @action(detail=True, methods=['get'])
    def employees(self, request, pk=None):
        """Get employees at this center"""
        center = self.get_object()
        employees = Employee.objects.filter(
            center=center, 
            user__is_active=True
        ).select_related('user').order_by('-rating')
        
        page = self.paginate_queryset(employees)
        if page is not None:
            serializer = EmployeeSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = EmployeeSerializer(employees, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def services(self, request, pk=None):
        """Get services available at this center"""
        center = self.get_object()
        services = ServiceCenter.objects.filter(
            center=center, 
            is_available=True
        ).select_related('service').order_by('service__name')
        
        serializer = ServiceCenterSerializer(services, many=True)
        return Response(serializer.data)

class ServiceCenterViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for ServiceCenter"""
    queryset = ServiceCenter.objects.filter(is_available=True).select_related(
        'service', 'center'
    ).order_by('service__name')
    serializer_class = ServiceCenterSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['center', 'service', 'is_available']

class EmployeeViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for Employee"""
    queryset = Employee.objects.filter(
        user__is_active=True, 
        is_verified=True
    ).select_related('user', 'center').order_by('-rating')
    
    serializer_class = EmployeeSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['designation', 'department', 'center', 'is_available']
    search_fields = ['user__first_name', 'user__last_name', 'employee_id', 
                    'specialization', 'skills']
    ordering_fields = ['rating', 'experience_years', 'tasks_completed']
    
    @action(detail=False, methods=['post'])
    def search(self, request):
        """Advanced employee search"""
        serializer = EmployeeSearchSerializer(data=request.data)
        if serializer.is_valid():
            employees = serializer.search()
            page = self.paginate_queryset(employees)
            if page is not None:
                serialized = self.get_serializer(page, many=True)
                return self.get_paginated_response(serialized.data)
            
            serialized = self.get_serializer(employees, many=True)
            return Response(serialized.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['get'])
    def availability(self, request, pk=None):
        """Get employee availability"""
        employee = self.get_object()
        availabilities = EmployeeAvailability.objects.filter(
            employee=employee
        ).order_by('date', 'start_time')[:7]  # Next 7 days
        
        serializer = EmployeeAvailabilitySerializer(availabilities, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def ratings(self, request, pk=None):
        """Get employee ratings"""
        employee = self.get_object()
        ratings = EmployeeRating.objects.filter(
            employee=employee
        ).select_related('user').order_by('-created_at')
        
        page = self.paginate_queryset(ratings)
        if page is not None:
            serializer = EmployeeRatingSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = EmployeeRatingSerializer(ratings, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def rate(self, request, pk=None):
        """Rate an employee"""
        employee = self.get_object()
        
        serializer = EmployeeRatingSerializer(
            data=request.data,
            context={'request': request}
        )
        
        if serializer.is_valid():
            serializer.save(employee=employee)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class EmployeeAvailabilityViewSet(viewsets.ModelViewSet):
    """ViewSet for EmployeeAvailability"""
    serializer_class = EmployeeAvailabilitySerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """Return availabilities for current user if employee"""
        user = self.request.user
        
        if hasattr(user, 'employee_profile'):
            return EmployeeAvailability.objects.filter(
                employee=user.employee_profile
            ).order_by('-date', 'start_time')
        
        return EmployeeAvailability.objects.none()
    
    def perform_create(self, serializer):
        """Set employee from user profile"""
        serializer.save(employee=self.request.user.employee_profile)

class EmployeeRatingViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for EmployeeRating (read-only for viewing)"""
    queryset = EmployeeRating.objects.all().select_related(
        'employee__user', 'user'
    ).order_by('-created_at')
    
    serializer_class = EmployeeRatingSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['employee', 'user', 'rating']

class TaskAssignmentViewSet(viewsets.ModelViewSet):
    """ViewSet for TaskAssignment"""
    serializer_class = TaskAssignmentSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """Return tasks based on user role"""
        user = self.request.user
        
        if user.is_staff or user.is_superuser:
            # Admin can see all tasks
            return TaskAssignment.objects.all().select_related(
                'employee__user', 'assigned_by', 'application'
            ).order_by('-created_at')
        
        if hasattr(user, 'employee_profile'):
            # Employee can see their own tasks
            return TaskAssignment.objects.filter(
                employee=user.employee_profile
            ).select_related('employee__user', 'assigned_by', 'application').order_by('-created_at')
        
        return TaskAssignment.objects.none()
    
    def perform_create(self, serializer):
        """Set assigned_by and validate permissions"""
        if not (self.request.user.is_staff or self.request.user.is_superuser):
            return Response(
                {"error": _("Only administrators can assign tasks.")},
                status=status.HTTP_403_FORBIDDEN
            )
        
        serializer.save(assigned_by=self.request.user)
    
    @action(detail=True, methods=['post'])
    def update_status(self, request, pk=None):
        """Update task status"""
        task = self.get_object()
        
        if not hasattr(request.user, 'employee_profile') or task.employee != request.user.employee_profile:
            return Response(
                {"error": _("Only assigned employee can update task status.")},
                status=status.HTTP_403_FORBIDDEN
            )
        
        new_status = request.data.get('status')
        if new_status not in dict(TaskAssignment.STATUS_CHOICES):
            return Response(
                {"error": _("Invalid status.")},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        task.status = new_status
        
        if new_status == 'completed':
            from django.utils import timezone
            task.completed_at = timezone.now()
        
        task.save()
        
        serializer = self.get_serializer(task)
        return Response(serializer.data)

class CenterSearchView(generics.GenericAPIView):
    """Center search endpoint"""
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    def post(self, request):
        """Search for centers"""
        serializer = CenterSearchSerializer(data=request.data)
        if serializer.is_valid():
            centers = serializer.search()
            
            # Paginate results
            page = self.paginate_queryset(centers)
            if page is not None:
                serialized = AkshayaCenterSerializer(page, many=True)
                return self.get_paginated_response(serialized.data)
            
            serialized = AkshayaCenterSerializer(centers, many=True)
            return Response(serialized.data)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class KozhikodeEmployeesView(generics.ListAPIView):
    """Get employees from Kozhikode district"""
    serializer_class = EmployeeSerializer
    
    def get_queryset(self):
        """Return Kozhikode employees"""
        return Employee.objects.filter(
            center__district='Kozhikode',
            user__is_active=True,
            is_verified=True
        ).select_related('user', 'center').order_by('user__first_name')