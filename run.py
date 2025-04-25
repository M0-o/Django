#!/usr/bin/env python3
"""
Django Project Launcher
-----------------------
This script checks if you're using Python 3 and helps launch the Django server.
"""

import sys
import os
import subprocess

def check_python_version():
    """Check if Python 3 is being used."""
    if sys.version_info[0] < 3:
        print("Error: This project requires Python 3.")
        print("You are using Python {}.{}.{}".format(
            sys.version_info[0], sys.version_info[1], sys.version_info[2]
        ))
        print("\nPlease use python3 instead of python to run this project.")
        return False
    return True

def run_django_server():
    """Run the Django development server."""
    try:
        # Run in the same process
        from django.core.management import execute_from_command_line
        execute_from_command_line(["manage.py", "runserver"])
    except ImportError:
        print("Django not installed. Installing dependencies...")
        try:
            subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], check=True)
            print("Dependencies installed. Starting server...")
            subprocess.run([sys.executable, "manage.py", "runserver"], check=True)
        except subprocess.CalledProcessError:
            print("Error installing dependencies or running server.")
            return False
    return True

def main():
    """Main entry point."""
    print("Starting Django Portfolio App...")
    
    if not check_python_version():
        return 1
    
    print(f"Using Python {sys.version}")
    
    # Change to script directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    
    if not run_django_server():
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main()) 