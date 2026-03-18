#!/usr/bin/env python
import os
import sys
import django

# Add current directory to path
sys.path.insert(0, os.path.dirname(__file__))

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'akshaya_backend.settings')
django.setup()

from django.core.management import execute_from_command_line

print("=" * 60)
print("AGADH MINIMAL SETUP")
print("=" * 60)

# Create database tables
print("\n1. Creating database tables...")
execute_from_command_line(['manage.py', 'makemigrations'])
execute_from_command_line(['manage.py', 'migrate'])

# Create admin user
print("\n2. Creating admin user...")
from django.contrib.auth import get_user_model
User = get_user_model()

if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser(
        username='admin',
        email='admin@agadh.kerala.gov.in',
        password='admin@123'
    )
    print("Admin user created:")
    print("Username: admin")
    print("Password: admin@123")
else:
    print("Admin user already exists")

print("\n" + "=" * 60)
print("SETUP COMPLETED!")
print("=" * 60)
print("\nRun the server with: python manage.py runserver 8000")
print("Access at: http://localhost:8000")
print("Admin at: http://localhost:8000/admin")