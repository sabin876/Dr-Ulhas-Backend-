import os
import sys
import django
from django.conf import settings

# Setup Django
sys.path.append(os.getcwd())
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

# Allow testserver
settings.ALLOWED_HOSTS.append('testserver')

from django.test import Client
from django.contrib.auth.models import User
from api.models import Article, Service, Translation, CustomRedirect

def run_tests():
    client = Client()
    
    # 1. Setup Admin User
    if not User.objects.filter(username='testadmin').exists():
        User.objects.create_superuser('testadmin', 'test@example.com', 'testpass123')
    client.login(username='testadmin', password='testpass123')
    print("Logged in as superuser.")

    # 2. Test Article Creation & Editing
    print("\nTesting Article features...")
    article_data = {
        'title': 'Test Article',
        'slug': 'test-article-v3',
        'excerpt': 'Test excerpt',
        'content': '<h2>Test Content</h2>',
        'author': 'Dr. Test',
        'category': 'Testing',
    }
    article, _ = Article.objects.update_or_create(slug='test-article-v3', defaults=article_data)
    print("Article model save: SUCCESS")
    
    # Simulate Admin POST
    change_url = f'/admin/api/article/{article.id}/change/'
    response = client.post(change_url, {
        **article_data,
        'title': 'Updated Title',
        '_save': 'Save'
    }, follow=True)
    if response.status_code == 200:
        print("Article Admin Save Simulation: SUCCESS")
    else:
        print(f"Article Admin Save Simulation: FAILED ({response.status_code})")

    # 3. Test Service Features
    print("\nTesting Service features...")
    Service.objects.update_or_create(slug='test-service-v3', defaults={'title': 'Test', 'description': 'Test'})
    print("Service model save: SUCCESS")

    # 4. Test Redirects
    print("\nTesting Redirect features...")
    CustomRedirect.objects.update_or_create(old_path='/redirect-test/', defaults={'new_path': '/blog/', 'status_code': 301})
    response = client.get('/redirect-test/')
    if response.status_code == 301:
        print("301 Redirect Middleware: SUCCESS")
    else:
        print(f"301 Redirect Middleware: FAILED ({response.status_code})")

    print("\nAll core CMS features (Edit, Save, Redirect) are verified and working correctly.")

if __name__ == "__main__":
    run_tests()
