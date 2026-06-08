from django.db import models
from django.utils.text import slugify

class SEOBaseModel(models.Model):
    meta_title = models.CharField(max_length=255, blank=True, null=True)
    meta_description = models.TextField(blank=True, null=True)
    canonical_url = models.URLField(max_length=500, blank=True, null=True, help_text="Leave blank to use the page's absolute URL")
    og_title = models.CharField(max_length=255, blank=True, null=True)
    og_description = models.TextField(blank=True, null=True)
    og_image = models.ImageField(upload_to='og_images/', blank=True, null=True)
    
    SCHEMA_CHOICES = [
        ('Article', 'Article'),
        ('MedicalBusiness', 'Medical Business / Local Business'),
        ('FAQPage', 'FAQ Page'),
        ('BreadcrumbList', 'Breadcrumbs'),
        ('None', 'Custom / None'),
    ]
    schema_type = models.CharField(max_length=50, choices=SCHEMA_CHOICES, default='None')
    schema_markup = models.JSONField(blank=True, null=True, help_text="JSON-LD schema markup")
    
    index_page = models.BooleanField(default=True, help_text="Should search engines index this page?")
    follow_links = models.BooleanField(default=True, help_text="Should search engines follow links on this page?")
    image_alt_text = models.CharField(max_length=255, blank=True, null=True, help_text="Alt text for the main image")
    h1_title = models.CharField(max_length=255, blank=True, null=True, help_text="Optional: Override the default H1 title")

    class Meta:
        abstract = True

    def get_canonical_url(self, request=None):
        if self.canonical_url:
            return self.canonical_url
        if request:
            return request.build_absolute_uri()
        return None

class Article(SEOBaseModel):
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    excerpt = models.TextField()
    content = models.TextField(help_text="HTML content for the blog post")
    image = models.ImageField(upload_to='articles/', blank=True, null=True)
    author = models.CharField(max_length=100, default="Dr. Ulhas Sonar")
    category = models.CharField(max_length=100)
    category_color = models.CharField(max_length=50, default="bg-blue-100 text-blue-600")
    date = models.DateField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

class Service(SEOBaseModel):
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    description = models.TextField()
    icon = models.CharField(max_length=100, default="activity", blank=True, help_text="Lucide icon name")
    image = models.ImageField(upload_to='services/', blank=True, null=True)
    items = models.JSONField(default=list, blank=True, help_text='Enter a JSON list, e.g., ["Feature 1", "Feature 2"]')
    faqs = models.JSONField(default=list, blank=True, help_text='Enter a list of FAQs, e.g. [{"question": "...", "answer": "..."}]')
    conditions = models.JSONField(default=list, blank=True, help_text='Enter a list of conditions, e.g., [{"id": 1, "title": "Back and neck pain", "description": "...", "icon": "<svg>..."}]')
    checklist_items = models.JSONField(default=list, blank=True, help_text='Enter a JSON list of strings, e.g., ["Item 1", "Item 2"]')
    tag_badges = models.JSONField(default=list, blank=True, help_text='Enter a JSON list of strings, e.g., ["Badge 1", "Badge 2"]')
    conditions_title = models.CharField(max_length=255, blank=True, null=True, help_text="Optional: Customize the conditions section heading")
    checklist_title = models.CharField(max_length=255, blank=True, null=True, help_text="Optional: Customize the checklist section heading")
    checklist_image = models.ImageField(upload_to='services/illustrations/', blank=True, null=True, help_text="Optional: Upload an illustration/image to replace the default therapist SVG")
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

class Translation(models.Model):
    key = models.CharField(max_length=255)
    language = models.CharField(max_length=10, choices=[('EN', 'English'), ('AR', 'Arabic'), ('HI', 'Hindi')])
    value = models.JSONField(help_text="The translated text or JSON object")

    class Meta:
        unique_together = ('key', 'language')

    def __str__(self):
        return f"{self.key} ({self.language})"

class SiteSetting(models.Model):
    robots_txt = models.TextField(default="User-agent: *\nAllow: /")
    header_scripts = models.TextField(blank=True, help_text="GSC, Google Analytics, etc.")
    footer_scripts = models.TextField(blank=True)
    internal_linking_rules = models.JSONField(default=dict, blank=True, help_text='Enter a JSON object, e.g., {"Knee Pain": "/services/knee-pain"}')
    hero_video = models.FileField(upload_to='videos/', blank=True, null=True, help_text="Upload the main hero section video")

    def __str__(self):
        return "Global Site Settings"

    class Meta:
        verbose_name = "Site Setting"
        verbose_name_plural = "Site Settings"

class CustomRedirect(models.Model):
    STATUS_CHOICES = [
        (301, '301 - Permanent Redirect'),
        (302, '302 - Temporary Redirect'),
        (410, '410 - Gone (Deleted)'),
        (451, '451 - Unavailable for Legal Reasons'),
    ]
    
    old_path = models.CharField(max_length=255, unique=True, help_text="e.g., /old-page/")
    new_path = models.CharField(max_length=255, blank=True, null=True, help_text="Leave blank for 410/451")
    status_code = models.IntegerField(choices=STATUS_CHOICES, default=301)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.old_path} -> {self.status_code}"

    class Meta:
        verbose_name = "Redirect"
        verbose_name_plural = "Redirects"


class GalleryItem(models.Model):
    CATEGORY_CHOICES = [
        ('Clinic', 'Clinic'),
        ('Surgery', 'Surgery'),
        ('Consultation', 'Consultation'),
        ('Awards', 'Awards'),
        ('Conference', 'Conference'),
        ('About', 'About'),
    ]

    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='gallery/', help_text="Upload the gallery image")
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='Clinic')
    span = models.CharField(max_length=50, default='col-span-1 row-span-1', help_text="Grid span layout, e.g. col-span-1 row-span-1, col-span-2 row-span-2")
    order = models.IntegerField(default=0, help_text="Display order (ascending)")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order', '-created_at']

    def __str__(self):
        return f"{self.title} ({self.category})"

