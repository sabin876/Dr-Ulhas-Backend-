import os
import json
import sys
import django
from django.utils.text import slugify

# Setup Django
sys.path.append(os.getcwd())
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from api.models import Article, Service, Translation, SiteSetting

def run_migration():
    json_path = 'data_dump.json'
    if not os.path.exists(json_path):
        print(f"File not found: {json_path}")
        return

    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # 1. Migrate Translations
    print("Migrating translations...")
    translations_data = data.get('translations', {})
    for lang_code, sections in translations_data.items():
        for section_key, section_data in sections.items():
            # We'll store each section as a separate Translation entry
            # or drill down deeper? Usually, drilling down to 2nd level is good.
            # e.g., key="nav", language="EN", value={...}
            Translation.objects.update_or_create(
                key=section_key,
                language=lang_code,
                defaults={'value': section_data}
            )
    print(f"Migrated {Translation.objects.count()} translation sections.")

    # 2. Migrate Articles
    print("Migrating articles...")
    articles_data = data.get('articles', {})
    for slug, article in articles_data.items():
        Article.objects.update_or_create(
            slug=slug,
            defaults={
                'title': article.get('title', ''),
                'excerpt': article.get('excerpt', ''),
                'content': article.get('content', ''),
                'author': article.get('author', 'Dr. Ulhas Sonar'),
                'category': article.get('category', 'Uncategorized'),
                'category_color': article.get('categoryColor', 'bg-blue-100 text-blue-600'),
                'meta_title': article.get('metaTitle', ''),
                'meta_description': article.get('metaDescription', ''),
                'index_page': True,
                'follow_links': True,
            }
        )
    print(f"Migrated {Article.objects.count()} articles.")

    # 3. Initialize Site Settings if not exists
    if not SiteSetting.objects.exists():
        SiteSetting.objects.create(
            robots_txt="User-agent: *\nAllow: /",
            header_scripts="<!-- GSC/GA scripts here -->"
        )
        print("Created default SiteSettings.")

if __name__ == "__main__":
    try:
        run_migration()
        print("Migration completed successfully!")
    except Exception as e:
        print(f"Migration failed: {e}")
