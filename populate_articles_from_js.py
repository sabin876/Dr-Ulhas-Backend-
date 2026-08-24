import os
import sys
import re
import django

sys.path.append(os.getcwd())
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from api.models import Article

js_filepath = r"C:\Users\DELL\OneDrive\Desktop\Dr Ulhas\Doctor-Port\src\constants\articlesData.js"

with open(js_filepath, 'r', encoding='utf-8') as f:
    js_content = f.read()

# Extract articles object content
match = re.search(r'export const articles = (\{[\s\S]*\});', js_content)
if not match:
    print("Could not find articles export in JS file")
    sys.exit(1)

articles_raw = match.group(1)

# Split articles by top-level keys like 'causes-of-knee-pain': {
# We can iterate through keys by matching `'([a-z0-9-]+)':\s*\{`
key_matches = list(re.finditer(r"'([a-z0-9-]+)':\s*\{", articles_raw))

print(f"Found {len(key_matches)} articles in articlesData.js")

for i, m in enumerate(key_matches):
    slug = m.group(1)
    start_idx = m.end()
    end_idx = key_matches[i+1].start() if i+1 < len(key_matches) else len(articles_raw)
    block = articles_raw[start_idx:end_idx]

    def get_field(field_name):
        f_match = re.search(rf'{field_name}:\s*["`]([\s\S]*?)["`]\s*,', block)
        if f_match:
            return f_match.group(1).strip()
        f_match2 = re.search(rf'{field_name}:\s*([^\n,]+),', block)
        if f_match2:
            val = f_match2.group(1).strip().strip('"\'')
            return val
        return ""

    title = get_field('title')
    meta_title = get_field('metaTitle')
    meta_description = get_field('metaDescription')
    author = get_field('author') or "Dr. Ulhas Sonar"
    category = get_field('category') or "General"
    category_color = get_field('categoryColor') or "bg-blue-100 text-blue-600"
    excerpt = get_field('excerpt')
    image = get_field('image')

    # Content extraction (multiline template literal)
    content_match = re.search(r'content:\s*`([\s\S]*?)`', block)
    content = content_match.group(1).strip() if content_match else ""

    if title:
        article, created = Article.objects.update_or_create(
            slug=slug,
            defaults={
                'title': title,
                'excerpt': excerpt,
                'content': content,
                'author': author,
                'category': category,
                'category_color': category_color,
                'meta_title': meta_title,
                'meta_description': meta_description,
                'image': image,
                'index_page': True,
                'follow_links': True,
            }
        )
        status = "Created" if created else "Updated"
        print(f"[{status}] Article: {slug} -> '{title}'")

print(f"Total articles in DB now: {Article.objects.count()}")
