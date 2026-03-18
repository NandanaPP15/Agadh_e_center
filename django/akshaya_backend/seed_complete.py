"""
Complete seed data for Agadh
"""
import os
import django
from django.contrib.auth.hashers import make_password
from django.utils import timezone

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'akshaya_backend.settings')
django.setup()

from users.models import User, UserProfile
from services.models import Service, ServiceCategory, ServiceStep, ServiceFAQ
from documents.models import DocumentType
from employees.models import AkshayaCenter, Employee

def create_admin():
    """Create admin user"""
    if not User.objects.filter(username='admin').exists():
        admin = User.objects.create(
            username='admin',
            email='admin@agadh.kerala.gov.in',
            password=make_password('admin@123'),
            first_name='Admin',
            last_name='User',
            user_type='admin',
            is_staff=True,
            is_superuser=True,
            is_active=True
        )
        UserProfile.objects.create(user=admin)
        print("✓ Admin user created")
    else:
        print("✓ Admin user already exists")

def create_test_users():
    """Create test users"""
    test_users = [
        {
            'username': 'citizen1',
            'email': 'rahul@example.com',
            'password': 'password123',
            'first_name': 'Rahul',
            'last_name': 'Kumar',
            'user_type': 'citizen',
            'phone': '9876543210',
            'district': 'Kozhikode'
        },
        {
            'username': 'citizen2',
            'email': 'anjali@example.com',
            'password': 'password123',
            'first_name': 'Anjali',
            'last_name': 'Nair',
            'user_type': 'citizen',
            'phone': '9876543211',
            'district': 'Kozhikode'
        },
        {
            'username': 'employee1',
            'email': 'nandana@akshaya.kerala.gov.in',
            'password': 'employee@123',
            'first_name': 'Nandana',
            'last_name': 'P P',
            'user_type': 'employee',
            'phone': 'xxxxxxxxx0',
            'district': 'Kozhikode'
        }
    ]
    
    for user_data in test_users:
        if not User.objects.filter(username=user_data['username']).exists():
            user = User.objects.create(
                username=user_data['username'],
                email=user_data['email'],
                password=make_password(user_data['password']),
                first_name=user_data['first_name'],
                last_name=user_data['last_name'],
                user_type=user_data['user_type'],
                phone=user_data['phone'],
                district=user_data['district']
            )
            UserProfile.objects.create(user=user)
            print(f"✓ User created: {user_data['username']}")
        else:
            print(f"✓ User already exists: {user_data['username']}")

def create_service_categories():
    """Create service categories"""
    categories = [
        {'name': 'Identity Documents', 'description': 'Government issued identity cards and certificates', 'icon': 'fa-id-card', 'color': '#4CAF50', 'order': 1},
        {'name': 'Personal Certificates', 'description': 'Birth, marriage, death and other personal certificates', 'icon': 'fa-certificate', 'color': '#2196F3', 'order': 2},
        {'name': 'Legal Documents', 'description': 'Legal certificates and clearances', 'icon': 'fa-gavel', 'color': '#FF9800', 'order': 3},
        {'name': 'Financial Services', 'description': 'Financial documents and certificates', 'icon': 'fa-rupee-sign', 'color': '#9C27B0', 'order': 4},
    ]
    
    for cat_data in categories:
        ServiceCategory.objects.get_or_create(
            name=cat_data['name'],
            defaults=cat_data
        )
    print("✓ Service categories created")

def create_services():
    """Create all 9 government services"""
    identity_category = ServiceCategory.objects.get(name='Identity Documents')
    personal_category = ServiceCategory.objects.get(name='Personal Certificates')
    legal_category = ServiceCategory.objects.get(name='Legal Documents')
    financial_category = ServiceCategory.objects.get(name='Financial Services')
    
    services_data = [
        {
            'name': 'Ration Card Services',
            'service_type': 'ration_card',
            'category': identity_category,
            'description': 'Apply for new ration card, modifications, transfers',
            'department': 'Civil Supplies Department',
            'processing_time': '7-10 working days',
            'fee': 50.00,
            'slug': 'ration-card',
            'icon': 'fa-id-card'
        },
        {
            'name': 'Marriage Registration',
            'service_type': 'marriage_registration',
            'category': personal_category,
            'description': 'Register marriages and obtain marriage certificates',
            'department': 'Local Administration',
            'processing_time': '3-5 working days',
            'fee': 100.00,
            'slug': 'marriage-registration',
            'icon': 'fa-ring'
        },
        {
            'name': 'Police Clearance Certificate',
            'service_type': 'police_clearance',
            'category': legal_category,
            'description': 'Obtain police clearance certificate for various purposes',
            'department': 'Kerala Police',
            'processing_time': '10-15 working days',
            'fee': 500.00,
            'slug': 'police-clearance',
            'icon': 'fa-shield-alt'
        },
        {
            'name': 'PAN Card Services',
            'service_type': 'pan_card',
            'category': financial_category,
            'description': 'Apply for new PAN card, corrections, and updates',
            'department': 'Income Tax Department',
            'processing_time': '15-20 working days',
            'fee': 107.00,
            'slug': 'pan-card',
            'icon': 'fa-address-card'
        },
        {
            'name': 'Birth Certificate Services',
            'service_type': 'birth_certificate',
            'category': personal_category,
            'description': 'Register births and obtain birth certificates',
            'department': 'Local Self Government',
            'processing_time': '3-7 working days',
            'fee': 30.00,
            'slug': 'birth-certificate',
            'icon': 'fa-baby'
        },
        {
            'name': 'Passport Services',
            'service_type': 'passport',
            'category': identity_category,
            'description': 'Apply for new passport and related services',
            'department': 'Ministry of External Affairs',
            'processing_time': '20-30 working days',
            'fee': 1500.00,
            'slug': 'passport',
            'icon': 'fa-passport'
        },
        {
            'name': 'Aadhaar Services',
            'service_type': 'aadhaar',
            'category': identity_category,
            'description': 'Aadhaar enrollment, updates, and corrections',
            'department': 'UIDAI',
            'processing_time': '15-20 working days',
            'fee': 0.00,
            'slug': 'aadhaar',
            'icon': 'fa-fingerprint'
        },
        {
            'name': 'Death Registration Services',
            'service_type': 'death_registration',
            'category': personal_category,
            'description': 'Register deaths and obtain death certificates',
            'department': 'Local Self Government',
            'processing_time': '3-7 working days',
            'fee': 30.00,
            'slug': 'death-registration',
            'icon': 'fa-cross'
        },
        {
            'name': 'Non-Creamy Layer Certificate',
            'service_type': 'ncl_certificate',
            'category': personal_category,
            'description': 'Apply for Non-Creamy Layer (OBC) certificate',
            'department': 'Revenue Department',
            'processing_time': '10-15 working days',
            'fee': 100.00,
            'slug': 'ncl-certificate',
            'icon': 'fa-certificate'
        }
    ]
    
    for service_data in services_data:
        service, created = Service.objects.get_or_create(
            service_type=service_data['service_type'],
            defaults=service_data
        )
        if created:
            print(f"✓ Service created: {service_data['name']}")
        else:
            print(f"✓ Service already exists: {service_data['name']}")

def create_document_types():
    """Create document types for services"""
    # Ration Card documents
    ration_service = Service.objects.get(service_type='ration_card')
    
    ration_docs = [
        {'name': 'Aadhaar Card', 'description': 'Aadhaar card of head of family', 'category': 'identity', 'is_mandatory': True},
        {'name': 'Address Proof', 'description': 'Electricity or water bill (last 3 months)', 'category': 'address', 'is_mandatory': True},
        {'name': 'Income Certificate', 'description': 'Income certificate from Tahsildar', 'category': 'income', 'is_mandatory': True},
        {'name': 'Family Member Proof', 'description': 'Aadhaar cards of all family members', 'category': 'family', 'is_mandatory': True},
        {'name': 'Photograph', 'description': 'Passport size photo of head of family', 'category': 'other', 'is_mandatory': True},
    ]
    
    for doc_data in ration_docs:
        DocumentType.objects.get_or_create(
            service=ration_service,
            name=doc_data['name'],
            defaults=doc_data
        )
    
    print("✓ Document types created")

def create_akshaya_center():
    """Create Kozhikode Akshaya Center"""
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
    if created:
        print("✓ Akshaya Center created")
    else:
        print("✓ Akshaya Center already exists")
    
    return center

def create_employees(center):
    """Create employees for Kozhikode center"""
    employees_data = [
        {
            'username': 'nandana',
            'first_name': 'Nandana',
            'last_name': 'P P',
            'employee_id': 'AKSH001',
            'designation': 'manager',
            'department': 'administration',
            'official_phone': 'xxxxxxxxx0',
            'rating': 4.8,
            'experience_years': 8
        },
        {
            'username': 'abhishna',
            'first_name': 'Abhishna',
            'last_name': 'P P',
            'employee_id': 'AKSH002',
            'designation': 'operator',
            'department': 'registration',
            'official_phone': 'xxxxxxxxx1',
            'rating': 4.6,
            'experience_years': 5
        },
        {
            'username': 'theja',
            'first_name': 'Theja',
            'last_name': 'K',
            'employee_id': 'AKSH003',
            'designation': 'assistant',
            'department': 'certificate',
            'official_phone': 'xxxxxxxxx2',
            'rating': 4.7,
            'experience_years': 4
        },
        {
            'username': 'maya',
            'first_name': 'Maya',
            'last_name': 'S',
            'employee_id': 'AKSH004',
            'designation': 'supervisor',
            'department': 'finance',
            'official_phone': 'xxxxxxxxx3',
            'rating': 4.9,
            'experience_years': 6
        },
        {
            'username': 'vandana',
            'first_name': 'Vandana',
            'last_name': 'T T K',
            'employee_id': 'AKSH005',
            'designation': 'coordinator',
            'department': 'support',
            'official_phone': 'xxxxxxxxx4',
            'rating': 4.5,
            'experience_years': 3
        }
    ]
    
    for emp_data in employees_data:
        user = User.objects.get(username=emp_data['username'])
        
        employee, created = Employee.objects.get_or_create(
            user=user,
            defaults={
                'employee_id': emp_data['employee_id'],
                'designation': emp_data['designation'],
                'department': emp_data['department'],
                'center': center,
                'official_email': f"{emp_data['username']}@akshaya.kerala.gov.in",
                'official_phone': emp_data['official_phone'],
                'rating': emp_data['rating'],
                'experience_years': emp_data['experience_years'],
                'is_verified': True,
                'is_available': True
            }
        )
        if created:
            print(f"✓ Employee created: {emp_data['first_name']} {emp_data['last_name']}")

def seed_all():
    """Run all seed functions"""
    print("=" * 60)
    print("SEEDING AGADH DATABASE")
    print("=" * 60)
    
    create_admin()
    create_test_users()
    create_service_categories()
    create_services()
    create_document_types()
    center = create_akshaya_center()
    create_employees(center)
    
    print("\n" + "=" * 60)
    print("DATABASE SEEDING COMPLETED!")
    print("=" * 60)
    print("\nLogin credentials:")
    print("Admin: admin / admin@123")
    print("Citizen: citizen1 / password123")
    print("Employee: nandana / employee@123")
    print("\nAccess URLs:")
    print("Frontend: http://localhost:8000")
    print("Admin: http://localhost:8000/admin")
    print("API: http://localhost:8000/api/services/")

if __name__ == '__main__':
    seed_all()