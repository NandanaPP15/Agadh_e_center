"""
URLs for Employees app
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    AkshayaCenterViewSet, ServiceCenterViewSet,
    EmployeeViewSet, EmployeeAvailabilityViewSet,
    EmployeeRatingViewSet, TaskAssignmentViewSet,
    CenterSearchView, KozhikodeEmployeesView
)

router = DefaultRouter()
router.register(r'centers', AkshayaCenterViewSet, basename='center')
router.register(r'service-centers', ServiceCenterViewSet, basename='servicecenter')
router.register(r'', EmployeeViewSet, basename='employee')
router.register(r'availabilities', EmployeeAvailabilityViewSet, basename='availability')
router.register(r'ratings', EmployeeRatingViewSet, basename='rating')
router.register(r'tasks', TaskAssignmentViewSet, basename='task')

urlpatterns = [
    path('', include(router.urls)),
    path('search/centers/', CenterSearchView.as_view(), name='center_search'),
    path('kozhikode/', KozhikodeEmployeesView.as_view(), name='kozhikode_employees'),
]