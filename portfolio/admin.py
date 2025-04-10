from django.contrib import admin
from .models import Template, Portfolio, Project

@admin.register(Template)
class TemplateAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_active', 'created_at')
    list_filter = ('is_active',)
    search_fields = ('name', 'description')

@admin.register(Portfolio)
class PortfolioAdmin(admin.ModelAdmin):
    list_display = ('user', 'title', 'contact_email', 'created_at', 'published')
    list_filter = ('created_at', 'published')
    search_fields = ('user__username', 'title', 'contact_email')
    raw_id_fields = ('user', 'template')
    prepopulated_fields = {'slug': ('title',)}

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'portfolio', 'completion_date', 'order')
    list_filter = ('completion_date', 'created_at')
    search_fields = ('title', 'description', 'technologies')
    raw_id_fields = ('portfolio',)
