from django.core.management.base import BaseCommand
from resumes.models import ResumeTemplate


class Command(BaseCommand):
    help = 'Seed default resume templates'

    def handle(self, *args, **options):
        templates = [
            {
                'name': 'Classic',
                'template_code': 'classic',
                'description': 'Traditional single-column layout with serif fonts. Perfect for conservative industries like law, finance, or government.',
                'is_premium': False,
            },
            {
                'name': 'Modern',
                'template_code': 'modern',
                'description': 'Two-column design with colored accents. Ideal for tech, creative, and startup roles.',
                'is_premium': False,
            },
        ]

        for template_data in templates:
            template, created = ResumeTemplate.objects.get_or_create(
                template_code=template_data['template_code'],
                defaults=template_data
            )
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f'Created template: {template.name}')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'Template already exists: {template.name}')
                )

        self.stdout.write(self.style.SUCCESS('Done!'))
