"""
Views for Documents app
"""
from rest_framework import viewsets, generics, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend
from django.utils.translation import gettext_lazy as _
from django.db.models import Q
from django.shortcuts import get_object_or_404

from .models import (
    DocumentType, UserDocument, SubmittedDocument,
    DocumentVerificationLog, DocumentTemplate
)
from .serializers import (
    DocumentTypeSerializer, UserDocumentSerializer,
    SubmittedDocumentSerializer, DocumentVerificationLogSerializer,
    DocumentTemplateSerializer, DocumentUploadSerializer,
    DocumentVerificationSerializer
)

class DocumentTypeViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for DocumentType"""
    queryset = DocumentType.objects.filter(is_active=True).select_related(
        'service'
    ).order_by('service__name', 'order', 'name')
    
    serializer_class = DocumentTypeSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['service', 'category', 'is_mandatory']
    search_fields = ['name', 'description', 'service__name']
    
    @action(detail=False, methods=['get'])
    def by_service(self, request):
        """Get documents by service slug"""
        service_slug = request.query_params.get('service_slug')
        if not service_slug:
            return Response(
                {"error": _("service_slug parameter is required.")},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        documents = DocumentType.objects.filter(
            service__slug=service_slug,
            is_active=True
        ).order_by('order', 'name')
        
        serializer = self.get_serializer(documents, many=True)
        return Response(serializer.data)

class UserDocumentViewSet(viewsets.ModelViewSet):
    """ViewSet for UserDocument"""
    serializer_class = UserDocumentSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['document_type', 'status', 'is_primary']
    search_fields = ['document_number', 'issuing_authority', 'document_type__name']
    ordering_fields = ['created_at', 'issue_date', 'expiry_date']
    
    def get_queryset(self):
        """Return documents for current user"""
        return UserDocument.objects.filter(
            user=self.request.user
        ).select_related('document_type__service').order_by('-created_at')
    
    def create(self, request, *args, **kwargs):
        """Upload new document"""
        serializer = DocumentUploadSerializer(data=request.data)
        if serializer.is_valid():
            # Create UserDocument from upload data
            document_data = serializer.validated_data.copy()
            document_data['user'] = request.user
            document_data['original_filename'] = document_data['file'].name
            
            user_document = UserDocument.objects.create(**document_data)
            
            return Response(
                UserDocumentSerializer(user_document).data,
                status=status.HTTP_201_CREATED
            )
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['post'])
    def verify(self, request, pk=None):
        """Verify a document (admin only)"""
        if not request.user.is_staff and not request.user.is_superuser:
            return Response(
                {"error": _("Only administrators can verify documents.")},
                status=status.HTTP_403_FORBIDDEN
            )
        
        document = self.get_object()
        
        serializer = DocumentVerificationSerializer(data=request.data)
        if serializer.is_valid():
            # Create verification log
            old_status = document.status
            new_status = serializer.validated_data['status']
            
            DocumentVerificationLog.objects.create(
                document=document,
                verified_by=request.user,
                old_status=old_status,
                new_status=new_status,
                notes=serializer.validated_data.get('notes', ''),
                verification_type='manual'
            )
            
            # Update document status
            document.status = new_status
            document.verified_by = request.user
            document.verification_date = serializer.validated_data.get('verification_date')
            
            if new_status == 'rejected':
                document.rejection_reason = serializer.validated_data.get('notes', '')
            
            document.save()
            
            return Response(
                UserDocumentSerializer(document).data,
                status=status.HTTP_200_OK
            )
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['get'])
    def expired(self, request):
        """Get expired documents"""
        from django.utils import timezone
        
        documents = self.get_queryset().filter(
            expiry_date__lt=timezone.now().date(),
            status='verified'
        )
        
        page = self.paginate_queryset(documents)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(documents, many=True)
        return Response(serializer.data)

class SubmittedDocumentViewSet(viewsets.ModelViewSet):
    """ViewSet for SubmittedDocument"""
    serializer_class = SubmittedDocumentSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """Return submitted documents for user's applications"""
        return SubmittedDocument.objects.filter(
            application__user=self.request.user
        ).select_related(
            'application', 'document_type', 'user_document'
        ).order_by('-created_at')
    
    def create(self, request, *args, **kwargs):
        """Submit document with application"""
        # Check if user has permission for this application
        application_id = request.data.get('application')
        if application_id:
            from services.models import ServiceApplication
            application = get_object_or_404(
                ServiceApplication, 
                id=application_id, 
                user=request.user
            )
        
        return super().create(request, *args, **kwargs)

class DocumentVerificationLogViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for DocumentVerificationLog (admin only)"""
    queryset = DocumentVerificationLog.objects.all().select_related(
        'document', 'verified_by'
    ).order_by('-created_at')
    
    serializer_class = DocumentVerificationLogSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['document', 'verified_by', 'verification_type', 'new_status']
    
    def get_queryset(self):
        """Restrict access to administrators"""
        if self.request.user.is_staff or self.request.user.is_superuser:
            return super().get_queryset()
        return DocumentVerificationLog.objects.none()

class DocumentTemplateViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for DocumentTemplate"""
    queryset = DocumentTemplate.objects.filter(is_active=True).prefetch_related(
        'services'
    ).order_by('name')
    
    serializer_class = DocumentTemplateSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['template_type', 'services']
    search_fields = ['name', 'description']
    
    @action(detail=True, methods=['get'])
    def download(self, request, pk=None):
        """Download template file"""
        template = self.get_object()
        
        if not template.template_file:
            return Response(
                {"error": _("Template file not available.")},
                status=status.HTTP_404_NOT_FOUND
            )
        
        # In production, you would serve the file
        return Response({
            "url": template.template_file.url,
            "name": template.name,
            "type": template.template_type
        })

class ServiceDocumentsView(generics.ListAPIView):
    """Get all documents required for a service"""
    serializer_class = DocumentTypeSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    def get_queryset(self):
        """Return documents for specified service"""
        service_slug = self.kwargs.get('slug')
        return DocumentType.objects.filter(
            service__slug=service_slug,
            is_active=True
        ).select_related('service').order_by('order', 'name')

class DocumentSearchView(generics.GenericAPIView):
    """Search documents"""
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        """Search user documents"""
        query = request.data.get('query', '').strip()
        document_type = request.data.get('document_type')
        status = request.data.get('status')
        
        documents = UserDocument.objects.filter(user=request.user)
        
        if query:
            documents = documents.filter(
                Q(document_number__icontains=query) |
                Q(issuing_authority__icontains=query) |
                Q(document_type__name__icontains=query) |
                Q(original_filename__icontains=query)
            )
        
        if document_type:
            documents = documents.filter(document_type_id=document_type)
        
        if status:
            documents = documents.filter(status=status)
        
        # Order by recent first
        documents = documents.order_by('-created_at')
        
        # Paginate results
        page = self.paginate_queryset(documents)
        if page is not None:
            serializer = UserDocumentSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = UserDocumentSerializer(documents, many=True)
        return Response(serializer.data)