"""
Models for Portfolio Builder Application

This file defines the database structure for the application using Django's ORM (Object-Relational Mapper).
Models are Python classes that map to database tables. Each attribute in the class represents a database field.

In Django's ORM:
- Each class inherits from models.Model and becomes a database table
- Each class attribute becomes a column in that table
- Relationships between tables are defined using ForeignKey, ManyToManyField, etc.
"""

from django.db import models  # Import Django's model system
from django.contrib.auth.models import User  # Import Django's built-in user model
from django.utils.text import slugify  # Import function to create URL-friendly slugs
import uuid  # Import uuid for generating unique identifiers

# Models are defined as Python classes that inherit from models.Model

class Template(models.Model):
    """
    Template Model
    
    Represents a portfolio design template that users can select.
    Each template has a name, description, thumbnail image, and active status.
    """
    # Each field is defined as a class attribute with a field type
    name = models.CharField(max_length=100)  # Text field with maximum length
    description = models.TextField()  # Unlimited text field for longer content
    thumbnail = models.ImageField(upload_to='templates/thumbnails/')  # Image field with upload path
    preview_url = models.URLField(blank=True)  # URL field that can be left empty (blank=True)
    is_active = models.BooleanField(default=True)  # Boolean field (true/false) with default value
    created_at = models.DateTimeField(auto_now_add=True)  # Automatically set to creation time
    
    @property  # Property decorator makes this method accessible as an attribute
    def feature_list(self):
        """
        Return list of features from description
        
        This splits the description text by line breaks and returns each line as an item in a list.
        Used to display features as bullet points in templates.
        """
        features = self.description.split('\n')  # Split text by newlines
        return [f.strip() for f in features if f.strip()]  # Remove whitespace and empty lines

    def __str__(self):
        """
        String representation of the model
        
        This method defines what text is shown when the object is printed or displayed.
        It's used in Django admin, shell, and debugging.
        """
        return self.name

class Portfolio(models.Model):
    """
    Portfolio Model
    
    Represents a user's portfolio with personal information, styling, and content.
    Each portfolio belongs to a user and uses a template for its design.
    """
    # Relationship fields link to other models
    user = models.ForeignKey(
        User,  # Link to Django's built-in User model
        on_delete=models.CASCADE,  # If user is deleted, delete their portfolios too
        related_name='portfolios'  # Allows user.portfolios.all() access
    )
    template = models.ForeignKey(
        Template,  # Link to our Template model
        on_delete=models.SET_NULL,  # If template is deleted, set to NULL
        null=True  # Allow NULL values in database
    )
    
    # Content fields
    title = models.CharField(max_length=200)  # Portfolio title/name
    about_me = models.TextField()  # Biographical information
    profile_image = models.ImageField(upload_to='portfolios/profile_images/')  # Profile photo
    
    # Contact information
    contact_email = models.EmailField()  # Email field with validation
    linkedin_url = models.URLField(blank=True)  # Optional LinkedIn URL
    github_url = models.URLField(blank=True)  # Optional GitHub URL
    
    # File attachments
    resume = models.FileField(
        upload_to='portfolios/resumes/',
        blank=True,  # Form field can be left empty
        null=True  # Database field can be NULL
    )
    
    # URL and status fields
    slug = models.SlugField(max_length=255, unique=True, blank=True)  # URL-friendly identifier
    published = models.BooleanField(default=False)  # Whether portfolio is public
    
    # Timestamp fields
    created_at = models.DateTimeField(auto_now_add=True)  # Set on creation
    updated_at = models.DateTimeField(auto_now=True)  # Updated on every save

    def save(self, *args, **kwargs):
        """
        Override the default save method
        
        This method is called when saving a portfolio object to the database.
        It generates a unique slug for new portfolios before saving.
        """
        if not self.slug:
            # Create a unique slug (URL-friendly identifier)
            base_slug = slugify(self.title)  # Convert title to URL-friendly format
            # Add random string to ensure uniqueness
            self.slug = f"{base_slug}-{uuid.uuid4().hex[:8]}"
        # Call the parent class's save method
        super().save(*args, **kwargs)

    def __str__(self):
        """String representation of the portfolio"""
        return f"{self.title} - {self.user.username}"

class Project(models.Model):
    """
    Project Model
    
    Represents a project within a portfolio.
    Each project belongs to a specific portfolio and contains details about the work.
    """
    # Relationship to Portfolio
    portfolio = models.ForeignKey(
        Portfolio,
        on_delete=models.CASCADE,  # If portfolio is deleted, delete all its projects
        related_name='projects'  # Allows portfolio.projects.all() access
    )
    
    # Basic information
    title = models.CharField(max_length=200)
    description = models.TextField()
    
    # Media and links
    image = models.ImageField(
        upload_to='portfolios/project_images/', 
        blank=True, 
        null=True
    )  # Project screenshot/image
    project_url = models.URLField(blank=True)  # Link to live project
    github_url = models.URLField(blank=True)  # Link to source code
    
    # Technical details
    technologies = models.CharField(
        max_length=500, 
        help_text="Enter technologies separated by commas"  # Help text shown in forms
    )
    completion_date = models.DateField(blank=True, null=True)  # When project was finished
    
    # Display order in portfolio
    order = models.IntegerField(default=1)  # Determines display order (1, 2, 3...)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        """
        Meta class for additional model options
        
        This defines model-wide settings that aren't fields.
        """
        ordering = ['order']  # Default ordering for queries
    
    @property
    def technologies_list(self):
        """
        Return list of technologies from comma-separated string
        
        This converts the comma-separated technologies string into a list
        for easier display in templates.
        """
        # Split by comma, strip whitespace, remove empty items
        return [tech.strip() for tech in self.technologies.split(',') if tech.strip()]

    def __str__(self):
        """String representation of the project"""
        return self.title
