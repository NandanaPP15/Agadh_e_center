"""
Simple seed data for Agadh
"""
import os
import django
from django.contrib.auth.hashers import make_password

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'akshaya_backend.settings')
django.setup()

from users.models import User, UserProfile

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
            'email': 'citizen1@example.com',
            'password': 'password123',
            'first_name': 'Rahul',
            'last_name': 'Kumar',
            'user_type': 'citizen',
            'phone': '9876543210',
            'district': 'Kozhikode'
        },
        {
            'username': 'citizen2',
            'email': 'citizen2@example.com',
            'password': 'password123',
            'first_name': 'Anjali',
            'last_name': 'Nair',
            'user_type': 'citizen',
            'phone': '9876543211',
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
            print(f"✓ Test user created: {user_data['username']}")
        else:
            print(f"✓ Test user already exists: {user_data['username']}")

if __name__ == '__main__':
    print("Seeding database...")
    create_admin()
    create_test_users()
    print("\nDatabase seeded successfully!")
    print("\nAdmin credentials:")
    print("Username: admin")
    print("Password: admin@123")
    print("\nTest user credentials:")
    print("Username: citizen1 / citizen2")
    print("Password: password123")