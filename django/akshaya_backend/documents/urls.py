"""
URLs for Documents app
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    DocumentTypeViewSet, UserDocumentViewSet,
    SubmittedDocumentViewSet, DocumentVerificationLogViewSet,
    DocumentTemplateViewSet, ServiceDocumentsView,
    DocumentSearchView
)

router = DefaultRouter()
router.register(r'types', DocumentTypeViewSet, basename='documenttype')
router.register(r'user', UserDocumentViewSet, basename='userdocument')
router.register(r'submitted', SubmittedDocumentViewSet, basename='submitteddocument')
router.register(r'verification-logs', DocumentVerificationLogViewSet, basename='verificationlog')
router.register(r'templates', DocumentTemplateViewSet, basename='template')

urlpatterns = [
    path('', include(router.urls)),
    path('search/', DocumentSearchView.as_view(), name='document_search'),
    path('service/<slug:slug>/', ServiceDocumentsView.as_view(), name='service_documents'),
]