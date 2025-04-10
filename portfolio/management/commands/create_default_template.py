from django.core.management.base import BaseCommand
from django.core.files.base import ContentFile
from portfolio.models import Template
import os

class Command(BaseCommand):
    help = 'Creates default portfolio templates'

    def handle(self, *args, **kwargs):
        # Create the Modern template
        if not Template.objects.filter(name='Modern').exists():
            template = Template(
                name='Modern',
                description='A clean, modern design with a professional look',
                is_active=True
            )
            
            # Create sample thumbnail
            thumbnail_content = """
            <svg width="300" height="200" xmlns="http://www.w3.org/2000/svg">
                <rect width="300" height="200" fill="#2c3e50"/>
                <text x="150" y="100" font-family="Arial" font-size="20" fill="white" text-anchor="middle">Modern Template</text>
            </svg>
            """
            thumbnail_file = ContentFile(thumbnail_content.strip().encode('utf-8'))
            template.thumbnail.save('modern_thumbnail.svg', thumbnail_file)
            
            # Save HTML template
            html_path = os.path.join('portfolio', 'templates', 'portfolio', 'templates', 'modern', 'template.html')
            if os.path.exists(html_path):
                with open(html_path, 'rb') as f:
                    html_content = f.read()
                template.html_template.save('modern_template.html', ContentFile(html_content))
            
            # Save CSS file
            css_path = os.path.join('portfolio', 'templates', 'portfolio', 'templates', 'modern', 'style.css')
            if os.path.exists(css_path):
                with open(css_path, 'rb') as f:
                    css_content = f.read()
                template.css_file.save('modern_style.css', ContentFile(css_content))
            
            template.save()
            self.stdout.write(self.style.SUCCESS('Successfully created Modern template'))
        else:
            self.stdout.write(self.style.WARNING('Modern template already exists'))

        # Create the Minimal template
        if not Template.objects.filter(name='Minimal').exists():
            template = Template(
                name='Minimal',
                description='Clean and modern design perfect for creatives',
                is_active=True
            )
            
            # Create sample thumbnail
            thumbnail_content = """
            <svg width="300" height="200" xmlns="http://www.w3.org/2000/svg">
                <rect width="300" height="200" fill="#f5f5f5"/>
                <rect x="50" y="50" width="200" height="100" fill="#ffffff" stroke="#000000" stroke-width="1"/>
                <text x="150" y="100" font-family="Arial" font-size="20" fill="black" text-anchor="middle">Minimal Template</text>
            </svg>
            """
            thumbnail_file = ContentFile(thumbnail_content.strip().encode('utf-8'))
            template.thumbnail.save('minimal_thumbnail.svg', thumbnail_file)
            
            # We'll use the same HTML/CSS as modern for now
            html_path = os.path.join('portfolio', 'templates', 'portfolio', 'templates', 'modern', 'template.html')
            if os.path.exists(html_path):
                with open(html_path, 'rb') as f:
                    html_content = f.read()
                template.html_template.save('minimal_template.html', ContentFile(html_content))
            
            css_path = os.path.join('portfolio', 'templates', 'portfolio', 'templates', 'modern', 'style.css')
            if os.path.exists(css_path):
                with open(css_path, 'rb') as f:
                    css_content = f.read()
                template.css_file.save('minimal_style.css', ContentFile(css_content))
            
            template.save()
            self.stdout.write(self.style.SUCCESS('Successfully created Minimal template'))
        else:
            self.stdout.write(self.style.WARNING('Minimal template already exists'))

        # Create the Creative template
        if not Template.objects.filter(name='Creative').exists():
            template = Template(
                name='Creative',
                description='Bold and artistic design for creative portfolios',
                is_active=True
            )
            
            # Create sample thumbnail
            thumbnail_content = """
            <svg width="300" height="200" xmlns="http://www.w3.org/2000/svg">
                <defs>
                    <linearGradient id="grad1" x1="0%" y1="0%" x2="100%" y2="100%">
                        <stop offset="0%" style="stop-color:#ff6b6b;stop-opacity:1" />
                        <stop offset="100%" style="stop-color:#6b66ff;stop-opacity:1" />
                    </linearGradient>
                </defs>
                <rect width="300" height="200" fill="url(#grad1)"/>
                <text x="150" y="100" font-family="Arial" font-size="20" fill="white" text-anchor="middle">Creative Template</text>
            </svg>
            """
            thumbnail_file = ContentFile(thumbnail_content.strip().encode('utf-8'))
            template.thumbnail.save('creative_thumbnail.svg', thumbnail_file)
            
            # We'll use the same HTML/CSS as modern for now
            html_path = os.path.join('portfolio', 'templates', 'portfolio', 'templates', 'modern', 'template.html')
            if os.path.exists(html_path):
                with open(html_path, 'rb') as f:
                    html_content = f.read()
                template.html_template.save('creative_template.html', ContentFile(html_content))
            
            css_path = os.path.join('portfolio', 'templates', 'portfolio', 'templates', 'modern', 'style.css')
            if os.path.exists(css_path):
                with open(css_path, 'rb') as f:
                    css_content = f.read()
                template.css_file.save('creative_style.css', ContentFile(css_content))
            
            template.save()
            self.stdout.write(self.style.SUCCESS('Successfully created Creative template'))
        else:
            self.stdout.write(self.style.WARNING('Creative template already exists'))

        # You can add more templates here in the future 