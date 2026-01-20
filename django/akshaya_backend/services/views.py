from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Service

class ServiceInfoAPIView(APIView):
    def get(self, request, service_name):
        try:
            service = Service.objects.get(name__iexact=service_name)
            return Response({
                "documents": service.documents,
                "processing_time": service.processing_time,
            })
        except Service.DoesNotExist:
            return Response(
                {"error": "Service not found"},
                status=status.HTTP_404_NOT_FOUND
            )
