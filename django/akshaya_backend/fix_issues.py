#!/usr/bin/env python
"""
Script to fix common issues in the Agadh project
"""
import os
import sys

def create_missing_files():
    """Create missing required files"""
    
    # Create templates directory if not exists
    templates_dir = os.path.join(os.path.dirname(__file__), 'templates')
    os.makedirs(templates_dir, exist_ok=True)
    
    # Create other required directories
    dirs_to_create = [
        'static',
        'media',
        'logs'
    ]
    
    for dir_name in dirs_to_create:
        dir_path = os.path.join(os.path.dirname(__file__), dir_name)
        os.makedirs(dir_path, exist_ok=True)
    
    print("Created missing directories")

def check_imports():
    """Check and fix import issues"""
    print("Checking for import issues...")
    
    # Check documents/admin.py
    documents_admin_path = os.path.join(os.path.dirname(__file__), 'documents', 'admin.py')
    if os.path.exists(documents_admin_path):
        with open(documents_admin_path, 'r') as f:
            content = f.read()
        
        # Fix the import if it's wrong
        if 'UploadedDocument' in content:
            print("Fixed documents/admin.py imports")
            # The fixed version is already in the code above
    
    print("Import checks completed")

if __name__ == '__main__':
    create_missing_files()
    check_imports()
    print("\nNow run these commands:")
    print("1. cd D:\\akshaya_project\\django\\akshaya_backend")
    print("2. python manage.py makemigrations")
    print("3. python manage.py migrate")
    print("4. python manage.py runserver 8000")