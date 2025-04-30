"""
Forms for Portfolio Builder Application

This file defines the forms used in the application using Django's forms framework.
Forms handle data validation, HTML rendering, and conversion between HTML forms and Python objects.

In Django forms:
- ModelForm connects forms directly to models, automating CRUD operations
- The Meta class specifies which model and fields to use
- Widgets customize the HTML rendering of form fields
- Form validation ensures data meets requirements before saving
"""

from django import forms  # Import Django's forms module
from django.contrib.auth.models import User  # Import Django's built-in User model
from .models import Portfolio, Project, Template  # Import our custom models

class PortfolioForm(forms.ModelForm):
    """
    Portfolio creation and editing form
    
    This form is used to create and edit portfolios. It automatically
    generates form fields based on the Portfolio model and applies
    Bootstrap styling to make the form look nice.
    """
    def __init__(self, *args, **kwargs):
        """
        Initialize the form
        
        This constructor method runs when a new form instance is created.
        It customizes form fields beyond what's defined in Meta.
        
        The *args and **kwargs allow passing any arguments to the parent constructor.
        """
        # Call the parent class's __init__ method first
        super().__init__(*args, **kwargs)
        
        # Customize template field to only show active templates
        self.fields['template'].queryset = Template.objects.filter(is_active=True)
        # Add Bootstrap class to template dropdown for styling
        self.fields['template'].widget.attrs['class'] = 'form-select'

    class Meta:
        """
        Configuration for the form
        
        The Meta class provides configuration details that apply to the entire form.
        """
        # Link this form to the Portfolio model
        model = Portfolio
        
        # Specify which model fields to include in the form
        fields = [
            'template', 'title', 'about_me', 'profile_image', 'contact_email',
            'linkedin_url', 'github_url', 'resume', 'published'
        ]
        
        # Customize the HTML widgets for each field
        # This adds Bootstrap classes and other attributes for styling and behavior
        widgets = {
            # Textarea for multi-line text with 4 rows and Bootstrap styling
            'about_me': forms.Textarea(attrs={'rows': 4, 'class': 'form-control'}),
            # File input for uploading images
            'profile_image': forms.FileInput(attrs={'class': 'form-control'}),
            # File input for uploading resume documents
            'resume': forms.FileInput(attrs={'class': 'form-control'}),
            # Email input with validation
            'contact_email': forms.EmailInput(attrs={'class': 'form-control'}),
            # URL inputs with validation
            'linkedin_url': forms.URLInput(attrs={'class': 'form-control'}),
            'github_url': forms.URLInput(attrs={'class': 'form-control'}),
            # Single-line text input
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            # Checkbox for boolean field
            'published': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

class ProjectForm(forms.ModelForm):
    """
    Project creation and editing form
    
    This form is used to create and edit projects within a portfolio.
    It connects to the Project model and applies Bootstrap styling.
    """
    class Meta:
        """Configuration for the form"""
        # Link this form to the Project model
        model = Project
        
        # Specify which model fields to include in the form
        fields = [
            'title', 'description', 'image', 'project_url',
            'github_url', 'technologies', 'completion_date',
            'order'
        ]
        
        # Customize the HTML widgets for each field
        widgets = {
            # Single-line text input for title
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            # Textarea for multi-line text with 5 rows
            'description': forms.Textarea(attrs={'rows': 5, 'class': 'form-control'}),
            # File input for uploading project images
            'image': forms.FileInput(attrs={'class': 'form-control'}),
            # URL inputs with validation
            'project_url': forms.URLInput(attrs={'class': 'form-control'}),
            'github_url': forms.URLInput(attrs={'class': 'form-control'}),
            # Text input for comma-separated technologies
            'technologies': forms.TextInput(attrs={'class': 'form-control'}),
            # Date input with HTML5 date picker
            'completion_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            # Number input with minimum value of 1
            'order': forms.NumberInput(attrs={'class': 'form-control', 'min': '1'}),
        }

class UserProfileForm(forms.ModelForm):
    """
    User profile editing form
    
    This form is used to edit user information like name and email.
    It connects to Django's built-in User model.
    """
    class Meta:
        """Configuration for the form"""
        # Link this form to Django's built-in User model
        model = User
        
        # Only include these fields from the User model
        # (Excludes username, password, etc.)
        fields = ['first_name', 'last_name', 'email']
        
        # Customize the HTML widgets for each field
        widgets = {
            # Text inputs with Bootstrap styling
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            # Email input with validation
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        } 