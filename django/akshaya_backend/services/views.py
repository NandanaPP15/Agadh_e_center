"""
Views for Services app
"""
from rest_framework import viewsets, generics, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from django.utils.translation import gettext_lazy as _
from django.db.models import Count, Q

from .models import Service, ServiceCategory, ServiceStep, ServiceFAQ, ServiceApplication
from .serializers import (
    ServiceSerializer, ServiceCategorySerializer,
    ServiceStepSerializer, ServiceFAQSerializer,
    ServiceApplicationSerializer, ServiceSearchSerializer
)
from .llm.intent_classifier import IntentClassifier

class ServiceCategoryViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for ServiceCategory"""
    queryset = ServiceCategory.objects.filter(is_active=True).annotate(
        service_count=Count('services')
    ).order_by('order', 'name')
    serializer_class = ServiceCategorySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

class ServiceViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for Service"""
    queryset = Service.objects.filter(is_active=True).select_related('category').prefetch_related(
        'steps', 'faqs', 'required_documents'
    ).order_by('-is_featured', 'name')
    serializer_class = ServiceSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category', 'service_type', 'online_available']
    search_fields = ['name', 'description', 'detailed_description']
    ordering_fields = ['name', 'popularity', 'created_at']
    lookup_field = 'slug'
    
    def retrieve(self, request, *args, **kwargs):
        """Retrieve service and increment popularity"""
        instance = self.get_object()
        instance.increment_popularity()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
    
    @action(detail=False, methods=['post'])
    def search(self, request):
        """Advanced search endpoint"""
        serializer = ServiceSearchSerializer(data=request.data)
        if serializer.is_valid():
            services = serializer.search()
            page = self.paginate_queryset(services)
            if page is not None:
                serialized = self.get_serializer(page, many=True)
                return self.get_paginated_response(serialized.data)
            
            serialized = self.get_serializer(services, many=True)
            return Response(serialized.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['get'])
    def similar(self, request, slug=None):
        """Get similar services"""
        service = self.get_object()
        similar = Service.objects.filter(
            Q(category=service.category) | Q(service_type=service.service_type),
            is_active=True
        ).exclude(id=service.id).order_by('-popularity')[:5]
        serializer = self.get_serializer(similar, many=True)
        return Response(serializer.data)

class ServiceStepViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for ServiceStep"""
    queryset = ServiceStep.objects.all().order_by('service', 'step_number')
    serializer_class = ServiceStepSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['service', 'is_online']

class ServiceFAQViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for ServiceFAQ"""
    queryset = ServiceFAQ.objects.all().order_by('order', 'id')
    serializer_class = ServiceFAQSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['service']

class ServiceApplicationViewSet(viewsets.ModelViewSet):
    """ViewSet for ServiceApplication"""
    serializer_class = ServiceApplicationSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """Return applications for current user"""
        return ServiceApplication.objects.filter(user=self.request.user).select_related(
            'service', 'user', 'assigned_to__user'
        ).order_by('-created_at')
    
    def perform_create(self, serializer):
        """Set user and generate reference"""
        serializer.save(user=self.request.user)
    
    @action(detail=True, methods=['post'])
    def submit(self, request, pk=None):
        """Submit application"""
        application = self.get_object()
        
        if application.status != ServiceApplication.DRAFT:
            return Response(
                {"error": _("Only draft applications can be submitted.")},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Validate required documents (simplified)
        # In production, check if all mandatory documents are uploaded
        
        application.status = ServiceApplication.SUBMITTED
        application.save()
        
        return Response({
            "message": _("Application submitted successfully."),
            "reference_number": application.reference_number
        })
    
    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        """Cancel application"""
        application = self.get_object()
        
        if application.status in [ServiceApplication.COMPLETED, ServiceApplication.CANCELLED]:
            return Response(
                {"error": _("Cannot cancel a completed or already cancelled application.")},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        application.status = ServiceApplication.CANCELLED
        application.save()
        
        return Response({"message": _("Application cancelled successfully.")})

class ChatbotQueryView(generics.GenericAPIView):
    """Chatbot query endpoint"""
    permission_classes = [permissions.AllowAny]  # Changed from IsAuthenticatedOrReadOnly
    
    def post(self, request):
        """Process chatbot query"""
        query = request.data.get('query', '').strip()
        language = request.data.get('language', 'en')
        
        if not query:
            return Response({"error": _("Query is required")}, 
                          status=status.HTTP_400_BAD_REQUEST)
        
        # Initialize intent classifier
        classifier = IntentClassifier()
        
        try:
            # Detect intent and process query
            intent = classifier.classify(query, language)
            
            # Get relevant services based on intent
            if intent.get('service_type'):
                services = Service.objects.filter(
                    service_type=intent['service_type'],
                    is_active=True
                )[:5]
                service_data = ServiceSerializer(services, many=True).data
            else:
                service_data = []
            
            # Prepare response
            response = {
                "intent": intent,
                "services": service_data,
                "message": intent.get('response', _("I found these services for you.")),
                "suggestions": intent.get('suggestions', [])
            }
            
            return Response(response)
            
        except Exception as e:
            # Log the error but return a friendly response
            import traceback
            print(f"Chatbot error: {e}")
            print(traceback.format_exc())
            
            return Response({
                "error": str(e),
                "message": _("I can help you with government services like Ration Card, Passport, Aadhaar, PAN Card, Marriage Registration, Police Clearance, Birth/Death Certificates, and NCL Certificate.")
            })
class ServiceDocumentView(generics.RetrieveAPIView):
    """Get service with required documents"""
    queryset = Service.objects.filter(is_active=True)
    serializer_class = ServiceSerializer
    lookup_field = 'slug'
    
    def retrieve(self, request, *args, **kwargs):
        """Get service with enhanced document information"""
        instance = self.get_object()
        instance.increment_popularity()
        
        # Get document information
        documents = instance.required_documents.all()
        document_data = []
        
        for doc in documents:
            document_data.append({
                'id': doc.id,
                'name': doc.name,
                'description': doc.description,
                'is_mandatory': doc.is_mandatory,
                'max_size_mb': doc.max_size_mb,
                'example_url': doc.example_url
            })
        
        response_data = self.get_serializer(instance).data
        response_data['required_documents'] = document_data
        
        return Response(response_data)