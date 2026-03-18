"""
Frontend URLs served by Django
"""
from django.urls import path
from django.views.generic import TemplateView

urlpatterns = [
    # Serve main frontend
    path('', TemplateView.as_view(template_name='index.html'), name='home'),
    
    # Service pages
    path('services/', TemplateView.as_view(template_name='services.html'), name='services'),
    path('services/<slug:slug>/', TemplateView.as_view(template_name='service_detail.html'), name='service_detail'),
    
    # Authentication pages
    path('login/', TemplateView.as_view(template_name='login.html'), name='login'),
    path('register/', TemplateView.as_view(template_name='register.html'), name='register'),
    path('profile/', TemplateView.as_view(template_name='profile.html'), name='profile'),
    
    # Application pages
    path('applications/', TemplateView.as_view(template_name='applications.html'), name='applications'),
    path('applications/<int:id>/', TemplateView.as_view(template_name='application_detail.html'), name='application_detail'),
    
    # Employee directory
    path('employees/', TemplateView.as_view(template_name='employees.html'), name='employees'),
    
    # About and contact
    path('about/', TemplateView.as_view(template_name='about.html'), name='about'),
    path('contact/', TemplateView.as_view(template_name='contact.html'), name='contact'),
    
    # Chatbot interface
    path('chatbot/', TemplateView.as_view(template_name='chatbot.html'), name='chatbot'),
]