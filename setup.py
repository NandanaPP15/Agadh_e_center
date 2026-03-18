"""
Agadh e-Center Digitization - Setup Script
Kerala Government Service Assistance Platform
"""
import os
import subprocess
import sys

def setup_project():
    """Setup complete project environment"""
    print("=" * 60)
    print("AGADH E-CENTER DIGITIZATION - SETUP")
    print("Kerala Government Service Assistance Platform")
    print("=" * 60)
    
    # Create project structure
    dirs = [
        "django/akshaya_backend",
        "django/akshaya_backend/akshaya_backend",
        "django/akshaya_backend/users",
        "django/akshaya_backend/services",
        "django/akshaya_backend/services/llm",
        "django/akshaya_backend/employees",
        "django/akshaya_backend/documents",
        "django/akshaya_backend/payments",
        "django/akshaya_backend/static",
        "django/akshaya_backend/media",
        "django/akshaya_backend/logs",
        "rasa_bot",
        "rasa_bot/actions",
        "rasa_bot/data",
        "rasa_bot/models",
        "frontend"
    ]
    
    for directory in dirs:
        os.makedirs(directory, exist_ok=True)
        print(f"Created: {directory}")
    
    print("\nProject structure created successfully!")
    print("\nNext steps:")
    print("1. Run: python setup.py install")
    print("2. Run: start.bat (Windows)")
    print("3. Access at: http://localhost:8000")
    
if __name__ == "__main__":
    setup_project()