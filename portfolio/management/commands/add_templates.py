from django.core.management.base import BaseCommand
from django.core.files.base import ContentFile
from portfolio.models import Template
import os
from django.conf import settings

class Command(BaseCommand):
    help = 'Add new portfolio templates to the database'

    def handle(self, *args, **options):
        templates_data = [
            {
                'name': 'Dark Mode',
                'description': 'A sleek dark theme with bold accent colors\nPerfect for developers and tech professionals\nHighlights your projects with striking contrast\nModern and stylish presentation',
                'thumbnail_filename': 'dark_mode_thumbnail.svg',
                'is_active': True
            },
            {
                'name': 'Gradient',
                'description': 'Beautiful gradient color scheme with modern design\nAnimated elements and smooth transitions\nEye-catching visual presentation\nPerfect for creative professionals',
                'thumbnail_filename': 'gradient_thumbnail.svg',
                'is_active': True
            },
            {
                'name': 'Minimalist',
                'description': 'Clean, minimal design with focus on content\nElegant typography and generous whitespace\nSubtle animations and interactions\nIdeal for photographers and writers',
                'thumbnail_filename': 'minimalist_thumbnail.svg',
                'is_active': True
            }
        ]
        
        for template_data in templates_data:
            # Check if template with this name already exists
            if Template.objects.filter(name=template_data['name']).exists():
                self.stdout.write(self.style.WARNING(f"Template '{template_data['name']}' already exists, skipping..."))
                continue
            
            # Create the template
            template = Template(
                name=template_data['name'],
                description=template_data['description'],
                is_active=template_data['is_active']
            )
            
            # Add thumbnail
            thumbnail_path = os.path.join(settings.MEDIA_ROOT, 'templates', 'thumbnails', template_data['thumbnail_filename'])
            if os.path.exists(thumbnail_path):
                with open(thumbnail_path, 'rb') as f:
                    thumbnail_content = f.read()
                    template.thumbnail.save(template_data['thumbnail_filename'], ContentFile(thumbnail_content), save=False)
            else:
                self.stdout.write(self.style.ERROR(f"Thumbnail file {thumbnail_path} not found!"))
                continue
            
            template.save()
            self.stdout.write(self.style.SUCCESS(f"Successfully added template '{template_data['name']}'"))
        
        self.stdout.write(self.style.SUCCESS(f"Template adding process completed.")) 