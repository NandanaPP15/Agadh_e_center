"""
Seed data for Agadh database
"""
import os
import django
from django.utils import timezone

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'akshaya_backend.settings')
django.setup()

from services.models import Service, ServiceCategory, ServiceStep, ServiceFAQ
from documents.models import DocumentType
from employees.models import AkshayaCenter, Employee
from users.models import User, UserProfile
from django.contrib.auth.hashers import make_password

def create_superuser():
    """Create superuser if not exists"""
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
        print("Superuser created: admin / admin@123")

def create_categories():
    """Create service categories"""
    categories = [
        {
            'name': 'Identity Documents',
            'description': 'Government issued identity cards and certificates',
            'icon': 'fa-id-card',
            'color': '#4CAF50',
            'order': 1
        },
        {
            'name': 'Personal Certificates',
            'description': 'Birth, marriage, death and other personal certificates',
            'icon': 'fa-certificate',
            'color': '#2196F3',
            'order': 2
        },
        {
            'name': 'Legal Documents',
            'description': 'Legal certificates and clearances',
            'icon': 'fa-gavel',
            'color': '#FF9800',
            'order': 3
        },
        {
            'name': 'Financial Services',
            'description': 'Financial documents and certificates',
            'icon': 'fa-rupee-sign',
            'color': '#9C27B0',
            'order': 4
        }
    ]
    
    for cat_data in categories:
        ServiceCategory.objects.get_or_create(
            name=cat_data['name'],
            defaults=cat_data
        )
    
    print("Service categories created")

def create_services():
    """Create all 9 government services with detailed information"""
    
    # Get categories
    identity_category = ServiceCategory.objects.get(name='Identity Documents')
    personal_category = ServiceCategory.objects.get(name='Personal Certificates')
    legal_category = ServiceCategory.objects.get(name='Legal Documents')
    financial_category = ServiceCategory.objects.get(name='Financial Services')
    
    services_data = [
        {
            'name': 'Ration Card Services',
            'service_type': Service.RATION_CARD,
            'category': identity_category,
            'description': 'Apply for new ration card, modifications, transfers, and related services',
            'detailed_description': 'Ration Card is issued by the Civil Supplies Department to households for purchasing food grains and other essential commodities at subsidized rates from the Public Distribution System (PDS).',
            'department': 'Civil Supplies Department',
            'processing_time': '7-10 working days',
            'fee': 50.00,
            'online_available': True,
            'offline_centers': 'All Akshaya Centers in Kerala',
            'slug': 'ration-card',
            'icon': 'fa-id-card',
            'is_featured': True,
            'steps': [
                {
                    'step_number': 1,
                    'title': 'Document Collection',
                    'description': 'Collect all required documents including identity proof, address proof, income certificate, and family member details',
                    'estimated_time': '1-2 days',
                    'is_online': False
                },
                {
                    'step_number': 2,
                    'title': 'Form Filling',
                    'description': 'Fill the ration card application form (Form 2) with accurate details',
                    'estimated_time': '30 minutes',
                    'is_online': True
                },
                {
                    'step_number': 3,
                    'title': 'Application Submission',
                    'description': 'Submit the application with documents at nearest Akshaya Center or online portal',
                    'estimated_time': '1-2 hours',
                    'is_online': True
                },
                {
                    'step_number': 4,
                    'title': 'Field Verification',
                    'description': 'Officials will verify details through field visit',
                    'estimated_time': '3-5 days',
                    'is_online': False
                },
                {
                    'step_number': 5,
                    'title': 'Card Issuance',
                    'description': 'Receive ration card at your address or collect from center',
                    'estimated_time': '2-3 days',
                    'is_online': False
                }
            ],
            'faqs': [
                {
                    'question': 'Who is eligible for ration card?',
                    'answer': 'Any Indian citizen residing in Kerala with valid address proof is eligible. The family income should be below the prescribed limit for different categories.',
                    'order': 1
                },
                {
                    'question': 'What are the types of ration cards?',
                    'answer': '1. Priority Household (PHH) - For poorest families\n2. Antyodaya Anna Yojana (AAY) - For poorest of the poor\n3. Non-Priority - For above poverty line families',
                    'order': 2
                },
                {
                    'question': 'Can I apply online?',
                    'answer': 'Yes, through the Akshaya e-Center portal or Civil Supplies Department website. However, document verification requires physical visit.',
                    'order': 3
                }
            ]
        },
        {
            'name': 'Marriage Registration',
            'service_type': Service.MARRIAGE_REGISTRATION,
            'category': personal_category,
            'description': 'Register marriages under Hindu Marriage Act, Special Marriage Act, and obtain marriage certificates',
            'detailed_description': 'Marriage registration is mandatory in Kerala. It provides legal recognition to marriages and the marriage certificate serves as proof for various purposes.',
            'department': 'Local Administration Department',
            'processing_time': '3-5 working days',
            'fee': 100.00,
            'online_available': True,
            'offline_centers': 'All Akshaya Centers and Local Self Government offices',
            'slug': 'marriage-registration',
            'icon': 'fa-ring',
            'is_featured': True,
            'steps': [
                {
                    'step_number': 1,
                    'title': 'Document Preparation',
                    'description': 'Collect required documents including age proof, address proof, photographs, and marriage proof',
                    'estimated_time': '2-3 days',
                    'is_online': False
                },
                {
                    'step_number': 2,
                    'title': 'Application Submission',
                    'description': 'Submit application at Registrar office or through Akshaya Center',
                    'estimated_time': '2-3 hours',
                    'is_online': True
                },
                {
                    'step_number': 3,
                    'title': 'Verification',
                    'description': 'Registrar verifies documents and may conduct interviews',
                    'estimated_time': '1-2 days',
                    'is_online': False
                },
                {
                    'step_number': 4,
                    'title': 'Certificate Issuance',
                    'description': 'Collect marriage certificate from office',
                    'estimated_time': '1 day',
                    'is_online': False
                }
            ]
        },
        {
            'name': 'Police Clearance Certificate',
            'service_type': Service.POLICE_CLEARANCE,
            'category': legal_category,
            'description': 'Obtain Police Clearance Certificate (PCC) for passport, employment, immigration purposes',
            'detailed_description': 'PCC is issued to Indian citizens who require a certificate of their criminal record or the lack thereof for various purposes.',
            'department': 'Kerala Police',
            'processing_time': '10-15 working days',
            'fee': 500.00,
            'online_available': True,
            'offline_centers': 'District Police Offices and Commissionerates',
            'slug': 'police-clearance',
            'icon': 'fa-shield-alt',
            'is_featured': False
        },
        {
            'name': 'PAN Card Services',
            'service_type': Service.PAN_CARD,
            'category': financial_category,
            'description': 'Apply for new PAN card, corrections, updates, and PAN-Aadhaar linking',
            'detailed_description': 'Permanent Account Number (PAN) is a 10-digit alphanumeric number issued by Income Tax Department. It is mandatory for financial transactions.',
            'department': 'Income Tax Department',
            'processing_time': '15-20 working days',
            'fee': 107.00,
            'online_available': True,
            'offline_centers': 'UTIITSL and NSDL centers',
            'slug': 'pan-card',
            'icon': 'fa-address-card',
            'is_featured': True
        },
        {
            'name': 'Birth Certificate Services',
            'service_type': Service.BIRTH_CERTIFICATE,
            'category': personal_category,
            'description': 'Register births, obtain birth certificates, duplicates, and corrections',
            'detailed_description': 'Birth registration is mandatory within 21 days of birth. Certificate serves as primary identity proof throughout life.',
            'department': 'Local Self Government Department',
            'processing_time': '3-7 working days',
            'fee': 30.00,
            'online_available': True,
            'offline_centers': 'Local bodies and Akshaya Centers',
            'slug': 'birth-certificate',
            'icon': 'fa-baby',
            'is_featured': True
        },
        {
            'name': 'Passport Services',
            'service_type': Service.PASSPORT,
            'category': identity_category,
            'description': 'Apply for new passport, renewal, reissue, and related services',
            'detailed_description': 'Indian Passport is issued by Ministry of External Affairs to Indian citizens for international travel.',
            'department': 'Ministry of External Affairs',
            'processing_time': '20-30 working days',
            'fee': 1500.00,
            'online_available': True,
            'offline_centers': 'Passport Seva Kendras and Post Offices',
            'slug': 'passport',
            'icon': 'fa-passport',
            'is_featured': True
        },
        {
            'name': 'Aadhaar Services',
            'service_type': Service.AADHAAR,
            'category': identity_category,
            'description': 'Aadhaar enrollment, updates, corrections, and child Aadhaar registration',
            'detailed_description': 'Aadhaar is a 12-digit unique identity number issued by UIDAI to Indian residents based on biometric and demographic data.',
            'department': 'Unique Identification Authority of India (UIDAI)',
            'processing_time': '15-20 working days',
            'fee': 0.00,
            'online_available': True,
            'offline_centers': 'Aadhaar Enrollment Centers and Akshaya Centers',
            'slug': 'aadhaar',
            'icon': 'fa-fingerprint',
            'is_featured': True
        },
        {
            'name': 'Death Registration Services',
            'service_type': Service.DEATH_REGISTRATION,
            'category': personal_category,
            'description': 'Register deaths, obtain death certificates, duplicates, and corrections',
            'detailed_description': 'Death registration is mandatory within 21 days of death. Certificate is required for legal and administrative purposes.',
            'department': 'Local Self Government Department',
            'processing_time': '3-7 working days',
            'fee': 30.00,
            'online_available': True,
            'offline_centers': 'Local bodies and Akshaya Centers',
            'slug': 'death-registration',
            'icon': 'fa-cross',
            'is_featured': False
        },
        {
            'name': 'Non-Creamy Layer Certificate',
            'service_type': Service.NCL_CERTIFICATE,
            'category': personal_category,
            'description': 'Apply for Non-Creamy Layer (OBC) certificate for reservation benefits',
            'detailed_description': 'NCL certificate is issued to Other Backward Classes whose family income is below ₹8 lakhs per annum.',
            'department': 'Revenue Department',
            'processing_time': '10-15 working days',
            'fee': 100.00,
            'online_available': True,
            'offline_centers': 'Tahsildar offices and Akshaya Centers',
            'slug': 'ncl-certificate',
            'icon': 'fa-certificate',
            'is_featured': False
        }
    ]
    
    for service_data in services_data:
        steps = service_data.pop('steps', [])
        faqs = service_data.pop('faqs', [])
        
        service, created = Service.objects.get_or_create(
            service_type=service_data['service_type'],
            defaults=service_data
        )
        
        if created:
            # Create steps
            for step_data in steps:
                ServiceStep.objects.create(service=service, **step_data)
            
            # Create FAQs
            for faq_data in faqs:
                ServiceFAQ.objects.create(service=service, **faq_data)
    
    print("Services created with steps and FAQs")

def create_document_types():
    """Create document types for all services"""
    
    # Ration Card Documents
    ration_service = Service.objects.get(service_type=Service.RATION_CARD)
    
    ration_documents = [
        {
            'name': 'Aadhaar Card (Head of Family)',
            'description': 'Aadhaar card of head of family',
            'category': 'identity',
            'is_mandatory': True,
            'max_size_mb': 2,
            'allowed_extensions': 'pdf,jpg,jpeg,png',
            'order': 1
        },
        {
            'name': 'Address Proof',
            'description': 'Electricity bill, water bill, or landline bill (last 3 months)',
            'category': 'address',
            'is_mandatory': True,
            'max_size_mb': 2,
            'allowed_extensions': 'pdf,jpg,jpeg,png',
            'order': 2
        },
        {
            'name': 'Family Member Aadhaar Cards',
            'description': 'Aadhaar cards of all family members',
            'category': 'family',
            'is_mandatory': True,
            'max_size_mb': 5,
            'allowed_extensions': 'pdf,jpg,jpeg,png',
            'order': 3
        },
        {
            'name': 'Income Certificate',
            'description': 'Income certificate from Tahsildar office',
            'category': 'income',
            'is_mandatory': True,
            'max_size_mb': 2,
            'allowed_extensions': 'pdf,jpg,jpeg',
            'order': 4
        },
        {
            'name': 'Passport Size Photograph',
            'description': 'Recent passport size photograph of head of family',
            'category': 'other',
            'is_mandatory': True,
            'max_size_mb': 1,
            'allowed_extensions': 'jpg,jpeg,png',
            'order': 5
        },
        {
            'name': 'Old Ration Card',
            'description': 'Previous ration card if any (for modification/transfer)',
            'category': 'other',
            'is_mandatory': False,
            'max_size_mb': 2,
            'allowed_extensions': 'pdf,jpg,jpeg,png',
            'order': 6
        }
    ]
    
    for doc_data in ration_documents:
        DocumentType.objects.get_or_create(
            service=ration_service,
            name=doc_data['name'],
            defaults=doc_data
        )
    
    # Marriage Registration Documents
    marriage_service = Service.objects.get(service_type=Service.MARRIAGE_REGISTRATION)
    
    marriage_documents = [
        {
            'name': 'Application Form',
            'description': 'Duly filled application form signed by both parties',
            'category': 'other',
            'is_mandatory': True,
            'max_size_mb': 2,
            'allowed_extensions': 'pdf,jpg,jpeg',
            'order': 1
        },
        {
            'name': 'Age Proof',
            'description': 'Birth certificate, SSLC certificate, or passport',
            'category': 'identity',
            'is_mandatory': True,
            'max_size_mb': 2,
            'allowed_extensions': 'pdf,jpg,jpeg,png',
            'order': 2
        },
        {
            'name': 'Address Proof',
            'description': 'Aadhaar card, voter ID, or utility bills',
            'category': 'address',
            'is_mandatory': True,
            'max_size_mb': 2,
            'allowed_extensions': 'pdf,jpg,jpeg,png',
            'order': 3
        },
        {
            'name': 'Passport Photographs',
            'description': '3 recent passport size photographs of each party',
            'category': 'other',
            'is_mandatory': True,
            'max_size_mb': 3,
            'allowed_extensions': 'jpg,jpeg,png',
            'order': 4
        },
        {
            'name': 'Marriage Proof',
            'description': 'Marriage invitation card or affidavit',
            'category': 'other',
            'is_mandatory': False,
            'max_size_mb': 2,
            'allowed_extensions': 'pdf,jpg,jpeg,png',
            'order': 5
        },
        {
            'name': 'Witness Details',
            'description': 'ID proof of 2 witnesses',
            'category': 'other',
            'is_mandatory': True,
            'max_size_mb': 2,
            'allowed_extensions': 'pdf,jpg,jpeg,png',
            'order': 6
        }
    ]
    
    for doc_data in marriage_documents:
        DocumentType.objects.get_or_create(
            service=marriage_service,
            name=doc_data['name'],
            defaults=doc_data
        )
    
    print("Document types created for services")

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
            'website': 'https://akshaya.kerala.gov.in',
            'status': 'active',
            'working_hours': '9:00 AM - 5:00 PM',
            'working_days': 'Monday to Saturday',
            'has_wifi': True,
            'has_printer': True,
            'has_scanner': True,
            'has_biometric': True,
            'has_wheelchair_access': True,
            'parking_available': True,
            'max_capacity': 100,
            'latitude': 11.2588,
            'longitude': 75.7804,
            'average_rating': 4.5,
            'total_ratings': 100,
            'govt_code': 'KER/AKSH/001',
            'nodal_officer': 'District Collector, Kozhikode'
        }
    )
    
    if created:
        print("Kozhikode Akshaya Center created")
    
    return center

def create_employees(center):
    """Create dummy employees for Kozhikode center"""
    employees_data = [
        {
            'username': 'nandana',
            'first_name': 'Nandana',
            'last_name': 'P P',
            'email': 'nandana@akshaya.kerala.gov.in',
            'password': 'employee@123',
            'phone': 'xxxxxxxxx0',
            'employee_id': 'AKSH-KZK-EMP-001',
            'designation': 'manager',
            'department': 'administration',
            'official_email': 'nandana.manager@akshaya.kerala.gov.in',
            'official_phone': 'xxxxxxxxx0',
            'specialization': 'Center Management, Public Service Delivery',
            'experience_years': 8,
            'skills': 'Management, Customer Service, Computer Operations',
            'rating': 4.8,
            'is_verified': True
        },
        {
            'username': 'abhishna',
            'first_name': 'Abhishna',
            'last_name': 'P P',
            'email': 'abhishna@akshaya.kerala.gov.in',
            'password': 'employee@123',
            'phone': 'xxxxxxxxx1',
            'employee_id': 'AKSH-KZK-EMP-002',
            'designation': 'operator',
            'department': 'registration',
            'official_email': 'abhishna.operator@akshaya.kerala.gov.in',
            'official_phone': 'xxxxxxxxx1',
            'specialization': 'Computer Operations, Data Entry',
            'experience_years': 5,
            'skills': 'Typing, Data Entry, Customer Support',
            'rating': 4.6,
            'is_verified': True
        },
        {
            'username': 'theja',
            'first_name': 'Theja',
            'last_name': 'K',
            'email': 'theja@akshaya.kerala.gov.in',
            'password': 'employee@123',
            'phone': 'xxxxxxxxx2',
            'employee_id': 'AKSH-KZK-EMP-003',
            'designation': 'assistant',
            'department': 'certificate',
            'official_email': 'theja.assistant@akshaya.kerala.gov.in',
            'official_phone': 'xxxxxxxxx2',
            'specialization': 'Document Verification, Certificate Services',
            'experience_years': 4,
            'skills': 'Documentation, Verification, Customer Service',
            'rating': 4.7,
            'is_verified': True
        },
        {
            'username': 'maya',
            'first_name': 'Maya',
            'last_name': 'S',
            'email': 'maya@akshaya.kerala.gov.in',
            'password': 'employee@123',
            'phone': 'xxxxxxxxx3',
            'employee_id': 'AKSH-KZK-EMP-004',
            'designation': 'supervisor',
            'department': 'finance',
            'official_email': 'maya.supervisor@akshaya.kerala.gov.in',
            'official_phone': 'xxxxxxxxx3',
            'specialization': 'Financial Services, Payment Processing',
            'experience_years': 6,
            'skills': 'Accounting, Payment Systems, Financial Management',
            'rating': 4.9,
            'is_verified': True
        },
        {
            'username': 'vandana',
            'first_name': 'Vandana',
            'last_name': 'T T K',
            'email': 'vandana@akshaya.kerala.gov.in',
            'password': 'employee@123',
            'phone': 'xxxxxxxxx4',
            'employee_id': 'AKSH-KZK-EMP-005',
            'designation': 'coordinator',
            'department': 'support',
            'official_email': 'vandana.coordinator@akshaya.kerala.gov.in',
            'official_phone': 'xxxxxxxxx4',
            'specialization': 'Customer Support, Service Coordination',
            'experience_years': 3,
            'skills': 'Communication, Problem Solving, Service Coordination',
            'rating': 4.5,
            'is_verified': True
        }
    ]
    
    for emp_data in employees_data:
        # Create user
        user_data = {k: v for k, v in emp_data.items() 
                    if k in ['username', 'first_name', 'last_name', 'email', 'password', 'phone']}
        user_data['password'] = make_password(user_data['password'])
        user_data['user_type'] = 'employee'
        
        user, created = User.objects.get_or_create(
            username=user_data['username'],
            defaults=user_data
        )
        
        if created:
            UserProfile.objects.create(user=user)
            
            # Create employee profile
            employee_data = {k: v for k, v in emp_data.items() 
                           if k in ['employee_id', 'designation', 'department', 
                                   'official_email', 'official_phone', 'specialization',
                                   'experience_years', 'skills', 'rating', 'is_verified']}
            employee_data['user'] = user
            employee_data['center'] = center
            
            Employee.objects.create(**employee_data)
    
    print("Employees created for Kozhikode center")

def seed_all():
    """Run all seed functions"""
    print("Starting database seeding...")
    
    create_superuser()
    create_categories()
    create_services()
    create_document_types()
    center = create_akshaya_center()
    create_employees(center)
    
    print("Database seeding completed successfully!")

if __name__ == '__main__':
    seed_all()