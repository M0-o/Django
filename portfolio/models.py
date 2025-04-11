from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
import uuid

# Create your models here.

class Template(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    thumbnail = models.ImageField(upload_to='thumbnails/')
    preview_url = models.URLField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    @property
    def feature_list(self):
        """Return list of features from description"""
        features = self.description.split('\n')
        return [f.strip() for f in features if f.strip()]

    def __str__(self):
        return self.name

class Portfolio(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='portfolios')
    template = models.ForeignKey(Template, on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=200)
    about_me = models.TextField()
    profile_image = models.ImageField(upload_to='profile_images/')
    contact_email = models.EmailField()
    linkedin_url = models.URLField(blank=True)
    github_url = models.URLField(blank=True)
    resume = models.FileField(upload_to='resumes/', blank=True, null=True)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    published = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            # Create a unique slug
            base_slug = slugify(self.title)
            self.slug = f"{base_slug}-{uuid.uuid4().hex[:8]}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.title} - {self.user.username}"

class Project(models.Model):
    portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE, related_name='projects')
    title = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to='project_images/', blank=True, null=True)
    project_url = models.URLField(blank=True)
    github_url = models.URLField(blank=True)
    technologies = models.CharField(max_length=500, help_text="Enter technologies separated by commas")
    completion_date = models.DateField(blank=True, null=True)
    order = models.IntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order']
    
    @property
    def technologies_list(self):
        """Return list of technologies from comma-separated string"""
        return [tech.strip() for tech in self.technologies.split(',') if tech.strip()]

    def __str__(self):
        return self.title
