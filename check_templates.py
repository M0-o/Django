#!/usr/bin/env python3
"""
Template validator script for Django Project
This script checks if all templates referenced in views exist
and validates paths to ensure there are no issues.
"""

import os
import re
import sys
from pathlib import Path

def find_template_references(views_file):
    """Find all render calls in views.py file and extract templates."""
    with open(views_file, 'r') as f:
        content = f.read()
    
    # Remove multi-line comment blocks ("""...""") that might contain render calls
    content = re.sub(r'""".*?"""', '', content, flags=re.DOTALL)
    
    # Remove single-line comments
    content = re.sub(r'#.*$', '', content, flags=re.MULTILINE)
    
    # Regular expression to find render calls with template references
    render_pattern = r'render\(\s*request\s*,\s*[\'"]([^\'"]+)[\'"]'
    template_refs = re.findall(render_pattern, content)
    
    return template_refs

def check_template_exists(template_name, template_dirs):
    """Check if a template exists in any of the template directories."""
    # Handle both 'app/template.html' and 'template.html' formats
    if '/' in template_name:
        parts = template_name.split('/')
        app_name = parts[0]
        template_path = '/'.join(parts[1:])
        
        for template_dir in template_dirs:
            # Check in app subdirectory
            full_path = os.path.join(template_dir, app_name, template_path)
            if os.path.exists(full_path):
                return True, full_path
            
            # Check directly at given path
            full_path = os.path.join(template_dir, template_name)
            if os.path.exists(full_path):
                return True, full_path
    else:
        # Just a template name without app prefix
        for template_dir in template_dirs:
            full_path = os.path.join(template_dir, template_name)
            if os.path.exists(full_path):
                return True, full_path
    
    return False, None

def main():
    # Configure paths
    BASE_DIR = Path(__file__).resolve().parent
    template_dirs = [
        os.path.join(BASE_DIR, 'portfolio/templates'),
        os.path.join(BASE_DIR, 'templates'),
    ]
    
    # Check if template directories exist
    for template_dir in template_dirs:
        if not os.path.exists(template_dir):
            print(f"Warning: Template directory not found: {template_dir}")
    
    # Find template references in views.py
    views_file = os.path.join(BASE_DIR, 'portfolio/views.py')
    if not os.path.exists(views_file):
        print(f"Error: Views file not found: {views_file}")
        return 1
    
    template_refs = find_template_references(views_file)
    print(f"Found {len(template_refs)} template references in views.py")
    
    # Check if templates exist
    missing_templates = []
    for template_ref in template_refs:
        exists, path = check_template_exists(template_ref, template_dirs)
        if exists:
            print(f"✓ Template exists: {template_ref} at {path}")
        else:
            print(f"✗ Template missing: {template_ref}")
            missing_templates.append(template_ref)
    
    if missing_templates:
        print("\nMissing templates:")
        for template in missing_templates:
            print(f"  - {template}")
        return 1
    else:
        print("\nAll templates found successfully!")
        return 0

if __name__ == "__main__":
    sys.exit(main()) 