import os
import sys
import django

# Add root folder to python path so 'core' can be imported
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Force database host to 127.0.0.1 to prevent IPv6 localhost resolution issues
os.environ['DB_HOST'] = '127.0.0.1'
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

django.setup()

from api.models import Service

def populate():
    # Find source service
    src = Service.objects.filter(slug='physiotherapy').first()
    if not src:
        print("Error: Source 'physiotherapy' service not found in database.")
        return

    # Targets to create/update
    targets = [
        ('test-physiotherapy', 'Test Physiotherapy'),
        ('test-physiotherapy-service', 'Test Physiotherapy Service')
    ]

    for slug, title in targets:
        service, created = Service.objects.update_or_create(
            slug=slug,
            defaults={
                'title': title,
                'description': src.description,
                'icon': src.icon,
                'image': src.image,
                'items': src.items,
                'faqs': src.faqs,
                'meta_title': f"{title} | Dr. Ulhas Sonar",
                'meta_description': src.meta_description,
                'index_page': False # Do not index test pages in search engines
            }
        )
        status = "Created" if created else "Updated"
        print(f"Successfully {status} service: '{title}' (slug: {slug})")

if __name__ == '__main__':
    populate()
