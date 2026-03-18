#!/usr/bin/env python
"""
Fix employee seeding
"""
import os
import django
from django.contrib.auth.hashers import make_password

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'akshaya_backend.settings')
django.setup()

from users.models import User, UserProfile
from employees.models import Employee, AkshayaCenter

def fix_employees():
    """Create employees if they don't exist"""
    print("Fixing employee data...")
    
    # First, create Akshaya Center if not exists
    center, created = AkshayaCenter.objects.get_or_create(
        center_code='AKSH-KZK-001',
        defaults={
            'name': 'Kozhikode Main Akshaya Center',
            'address': 'Near Civil Station, Kozhikode',
            'location': 'Kozhikode',
            'district': 'Kozhikode',
            'pincode': '673020',
            'phone': '0495-1234567',
            'email': 'kozhikode@akshaya.kerala.gov.in',
            'status': 'active',
            'working_hours': '9:00 AM - 5:00 PM',
            'working_days': 'Monday to Saturday',
            'has_wifi': True,
            'has_printer': True,
            'has_scanner': True,
            'has_biometric': True,
            'max_capacity': 100
        }
    )
    print(f"Akshaya Center: {'Created' if created else 'Already exists'}")
    
    # Employee data
    employees_data = [
        {
            'username': 'nandana',
            'first_name': 'Nandana',
            'last_name': 'P P',
            'email': 'nandana@akshaya.kerala.gov.in',
            'password': 'employee@123',
            'phone': '9876543210',
            'employee_id': 'AKSH001',
            'designation': 'manager',
            'department': 'administration',
            'official_phone': '9876543210',
            'rating': 4.8,
            'experience_years': 8
        },
        {
            'username': 'abhishna',
            'first_name': 'Abhishna',
            'last_name': 'P P',
            'email': 'abhishna@akshaya.kerala.gov.in',
            'password': 'employee@123',
            'phone': '9876543211',
            'employee_id': 'AKSH002',
            'designation': 'operator',
            'department': 'registration',
            'official_phone': '9876543211',
            'rating': 4.6,
            'experience_years': 5
        },
        {
            'username': 'theja',
            'first_name': 'Theja',
            'last_name': 'K',
            'email': 'theja@akshaya.kerala.gov.in',
            'password': 'employee@123',
            'phone': '9876543212',
            'employee_id': 'AKSH003',
            'designation': 'assistant',
            'department': 'certificate',
            'official_phone': '9876543212',
            'rating': 4.7,
            'experience_years': 4
        },
        {
            'username': 'maya',
            'first_name': 'Maya',
            'last_name': 'S',
            'email': 'maya@akshaya.kerala.gov.in',
            'password': 'employee@123',
            'phone': '9876543213',
            'employee_id': 'AKSH004',
            'designation': 'supervisor',
            'department': 'finance',
            'official_phone': '9876543213',
            'rating': 4.9,
            'experience_years': 6
        },
        {
            'username': 'vandana',
            'first_name': 'Vandana',
            'last_name': 'T T K',
            'email': 'vandana@akshaya.kerala.gov.in',
            'password': 'employee@123',
            'phone': '9876543214',
            'employee_id': 'AKSH005',
            'designation': 'coordinator',
            'department': 'support',
            'official_phone': '9876543214',
            'rating': 4.5,
            'experience_years': 3
        }
    ]
    
    for emp_data in employees_data:
        # Create or get user
        user, created = User.objects.get_or_create(
            username=emp_data['username'],
            defaults={
                'email': emp_data['email'],
                'first_name': emp_data['first_name'],
                'last_name': emp_data['last_name'],
                'password': make_password(emp_data['password']),
                'phone': emp_data['phone'],
                'user_type': 'employee'
            }
        )
        
        if created:
            UserProfile.objects.create(user=user)
            print(f"Created user: {emp_data['username']}")
        
        # Create or get employee
        employee, created = Employee.objects.get_or_create(
            user=user,
            defaults={
                'employee_id': emp_data['employee_id'],
                'designation': emp_data['designation'],
                'department': emp_data['department'],
                'center': center,
                'official_email': emp_data['email'],
                'official_phone': emp_data['official_phone'],
                'rating': emp_data['rating'],
                'experience_years': emp_data['experience_years'],
                'is_verified': True,
                'is_available': True
            }
        )
        
        if created:
            print(f"Created employee: {emp_data['first_name']} {emp_data['last_name']}")
        else:
            print(f"Employee already exists: {emp_data['first_name']}")
    
    print("\nEmployee data fixed successfully!")
    print(f"Total employees: {Employee.objects.count()}")
    print(f"Kozhikode employees: {Employee.objects.filter(center=center).count()}")

if __name__ == '__main__':
    fix_employees()