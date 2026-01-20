from django.urls import path
from .views import ServiceInfoAPIView

urlpatterns = [
    path("info/<str:service_name>/", ServiceInfoAPIView.as_view()),
]
