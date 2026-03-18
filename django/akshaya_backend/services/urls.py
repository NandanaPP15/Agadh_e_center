"""
URLs for Services app
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    ServiceCategoryViewSet, ServiceViewSet,
    ServiceStepViewSet, ServiceFAQViewSet,
    ServiceApplicationViewSet, ChatbotQueryView,
    ServiceDocumentView
)

router = DefaultRouter()
router.register(r'categories', ServiceCategoryViewSet, basename='category')
router.register(r'', ServiceViewSet, basename='service')
router.register(r'steps', ServiceStepViewSet, basename='step')
router.register(r'faqs', ServiceFAQViewSet, basename='faq')
router.register(r'applications', ServiceApplicationViewSet, basename='application')

urlpatterns = [
    path('', include(router.urls)),
    path('chatbot/query/', ChatbotQueryView.as_view(), name='chatbot_query'),
    path('<slug:slug>/documents/', ServiceDocumentView.as_view(), name='service_documents'),
]