#!/usr/bin/env python
"""
Reset and setup Agadh project
"""
import os
import sys
import shutil
import subprocess

def clean_project():
    """Clean project files"""
    print("Cleaning project...")
    
    # Remove database
    db_file = os.path.join(os.path.dirname(__file__), 'db.sqlite3')
    if os.path.exists(db_file):
        os.remove(db_file)
        print("Removed database")
    
    # Remove migrations directories
    apps = ['users', 'services', 'employees', 'documents', 'payments']
    for app in apps:
        migrations_dir = os.path.join(os.path.dirname(__file__), app, 'migrations')
        if os.path.exists(migrations_dir):
            # Keep __init__.py but remove other files
            for item in os.listdir(migrations_dir):
                item_path = os.path.join(migrations_dir, item)
                if item != '__init__.py' and not item.startswith('.'):
                    if os.path.isfile(item_path):
                        os.remove(item_path)
                    else:
                        shutil.rmtree(item_path)
            print(f"Cleaned migrations for {app}")
    
    # Remove pycache directories
    for root, dirs, files in os.walk(os.path.dirname(__file__)):
        for dir in dirs:
            if dir == '__pycache__':
                pycache_path = os.path.join(root, dir)
                shutil.rmtree(pycache_path)
                print(f"Removed {pycache_path}")

def setup_project():
    """Setup project"""
    print("\nSetting up project...")
    
    # Run migrations
    print("Running migrations...")
    subprocess.run([sys.executable, 'manage.py', 'makemigrations'], check=True)
    subprocess.run([sys.executable, 'manage.py', 'migrate'], check=True)
    
    # Create superuser
    print("\nCreating superuser...")
    print("Username: admin")
    print("Email: admin@agadh.kerala.gov.in")
    print("Password: admin@123")
    
    from django.contrib.auth import get_user_model
    User = get_user_model()
    
    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser(
            username='admin',
            email='admin@agadh.kerala.gov.in',
            password='admin@123'
        )
        print("Superuser created successfully!")
    else:
        print("Superuser already exists")
    
    # Load seed data
    print("\nLoading seed data...")
    seed_path = os.path.join(os.path.dirname(__file__), 'seed_data.py')
    if os.path.exists(seed_path):
        subprocess.run([sys.executable, 'manage.py', 'shell', '-c', 
                       'exec(open("seed_data.py").read())'])
        print("Seed data loaded successfully!")
    else:
        print("Seed data file not found")

def check_dependencies():
    """Check if all dependencies are installed"""
    print("\nChecking dependencies...")
    
    try:
        import django
        print(f"✓ Django {django.__version__}")
    except ImportError:
        print("✗ Django not installed")
        return False
    
    try:
        import rest_framework
        print("✓ Django REST Framework")
    except ImportError:
        print("✗ Django REST Framework not installed")
        return False
    
    try:
        import corsheaders
        print("✓ Django CORS Headers")
    except ImportError:
        print("✗ Django CORS Headers not installed")
        return False
    
    try:
        import drf_yasg
        print("✓ DRF YASG")
    except ImportError:
        print("✗ DRF YASG not installed")
        return False
    
    return True

if __name__ == '__main__':
    print("=" * 60)
    print("AGADH E-CENTER DIGITIZATION - SETUP")
    print("=" * 60)
    
    # Add current directory to Python path
    sys.path.insert(0, os.path.dirname(__file__))
    
    # Set Django settings
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'akshaya_backend.settings')
    
    try:
        import django
        django.setup()
        
        if check_dependencies():
            clean_project()
            setup_project()
            
            print("\n" + "=" * 60)
            print("SETUP COMPLETED SUCCESSFULLY!")
            print("=" * 60)
            print("\nTo start the server, run:")
            print("python manage.py runserver 8000")
            print("\nAccess the application at: http://localhost:8000")
            print("Admin panel: http://localhost:8000/admin")
            print("API Documentation: http://localhost:8000/swagger")
        else:
            print("\nPlease install missing dependencies:")
            print("pip install -r requirements.txt")
            
    except Exception as e:
        print(f"\nError during setup: {e}")
        print("\nTrying alternative setup method...")
        
        # Try direct commands
        try:
            clean_project()
            subprocess.run([sys.executable, 'manage.py', 'makemigrations'], check=False)
            subprocess.run([sys.executable, 'manage.py', 'migrate'], check=False)
            
            print("\nSetup completed! Now run:")
            print("python manage.py createsuperuser")
            print("python manage.py runserver 8000")
        except Exception as e2:
            print(f"Alternative setup failed: {e2}")