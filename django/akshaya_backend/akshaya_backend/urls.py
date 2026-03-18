"""
URL configuration for akshaya_backend project.
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="Agadh API",
        default_version='v1',
        description="Agadh e-Center Digitization Platform API",
        contact=openapi.Contact(email="support@agadh.kerala.gov.in"),
        license=openapi.License(name="Kerala Government License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),
    
    # API Documentation
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    
    # API Endpoints
    path('api/auth/', include('users.urls')),
    path('api/services/', include('services.urls')),
    path('api/employees/', include('employees.urls')),
    path('api/documents/', include('documents.urls')),
    path('api/payments/', include('payments.urls')),
    
    # Frontend
    path('', include('services.frontend_urls')),
]

# Serve static and media files in development
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)