from django.core.management.base import BaseCommand
from django.utils.text import slugify
from portfolio.models import Portfolio
import uuid

class Command(BaseCommand):
    help = 'Fix missing portfolio slugs'

    def handle(self, *args, **options):
        portfolios_without_slug = Portfolio.objects.filter(slug__exact='')
        self.stdout.write(f"Found {portfolios_without_slug.count()} portfolios with empty slugs")

        # Also check for NULL slugs if your database allows it (though the model has blank=True, not null=True)
        portfolios_with_null_slug = Portfolio.objects.filter(slug__isnull=True)
        self.stdout.write(f"Found {portfolios_with_null_slug.count()} portfolios with NULL slugs")

        # Combine the querysets and process
        portfolios_to_fix = portfolios_without_slug | portfolios_with_null_slug
        
        fixed_count = 0
        for portfolio in portfolios_to_fix:
            # Only generate a slug if the title exists
            if portfolio.title:
                base_slug = slugify(portfolio.title)
                portfolio.slug = f"{base_slug}-{uuid.uuid4().hex[:8]}"
                portfolio.save(update_fields=['slug'])
                fixed_count += 1
                self.stdout.write(f"Fixed portfolio '{portfolio.title}' with new slug: {portfolio.slug}")
            else:
                self.stdout.write(self.style.WARNING(
                    f"Portfolio ID {portfolio.id} has no title. Please add a title and then a slug will be generated."
                ))
        
        self.stdout.write(self.style.SUCCESS(f"Fixed {fixed_count} portfolios with missing slugs!")) 