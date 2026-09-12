from unfold.admin import ModelAdmin, TabularInline, StackedInline
from unfold.decorators import display
from django.contrib import admin
from django import forms
from django.utils.html import format_html
from django.urls import reverse
from ckeditor.widgets import CKEditorWidget
from .models import Article, Service, SubService, Translation, SiteSetting, CustomRedirect, GalleryItem, HeroVideo, SecondOpinion, HomePage, SportingInjurySection, ServicesPage
from django.contrib.auth.models import Group, User

try:
    admin.site.unregister(Group)
    admin.site.unregister(User)
except admin.sites.NotRegistered:
    pass

from .widgets import ListStringWidget, ConditionsWidget, CommonlyTreatedWidget, JourneyStepsWidget, FaqWidget, SportsInjuryItemsWidget, TrustCardsWidget, HeroStatsWidget, SchemaJSONFormField, SchemaMarkupWidget

class SEOBaseAdminForm(forms.ModelForm):
    schema_markup = SchemaJSONFormField(
        required=False,
        label="Schema Markup (JSON-LD)",
        help_text="Structured JSON-LD schema markup. You can paste raw JSON or the full &lt;script type=\"application/ld+json\"&gt;...&lt;/script&gt; snippet."
    )

class ArticleAdminForm(SEOBaseAdminForm):
    class Meta:
        model = Article
        fields = "__all__"
        widgets = {
            "content": CKEditorWidget(),
            "faqs": FaqWidget(),
        }

class ServiceAdminForm(SEOBaseAdminForm):
    class Meta:
        model = Service
        fields = "__all__"
        widgets = {
            "description": CKEditorWidget(),
            "about_description": CKEditorWidget(),
            "highlight_description": CKEditorWidget(),
            "highlight_doctor_description": CKEditorWidget(),
            "items": ListStringWidget(),
            "conditions": ConditionsWidget(),
            "checklist_items": ListStringWidget(),
            "tag_badges": ListStringWidget(),
            "who_needs_items": ListStringWidget(),
            "commonly_treated": CommonlyTreatedWidget(),
            "highlight_checklist_items": ListStringWidget(),
            "highlight_doctor_badges": ListStringWidget(),
            "journey_steps": JourneyStepsWidget(),
            "faqs": FaqWidget(),
        }


    def clean_items(self):
        val = self.cleaned_data.get('items')
        if val is None or val == "":
            return []
        return val

    def clean_conditions(self):
        val = self.cleaned_data.get('conditions')
        if val is None or val == "":
            return []
        return val

    def clean_checklist_items(self):
        val = self.cleaned_data.get('checklist_items')
        if val is None or val == "":
            return []
        return val

    def clean_tag_badges(self):
        val = self.cleaned_data.get('tag_badges')
        if val is None or val == "":
            return []
        return val

    def clean_who_needs_items(self):
        val = self.cleaned_data.get('who_needs_items')
        if val is None or val == "":
            return []
        return val

    def clean_commonly_treated(self):
        val = self.cleaned_data.get('commonly_treated')
        if val is None or val == "":
            return []
        return val

    def clean_highlight_checklist_items(self):
        val = self.cleaned_data.get('highlight_checklist_items')
        if val is None or val == "":
            return []
        return val

    def clean_highlight_doctor_badges(self):
        val = self.cleaned_data.get('highlight_doctor_badges')
        if val is None or val == "":
            return []
        return val

    def clean_journey_steps(self):
        val = self.cleaned_data.get('journey_steps')
        if val is None or val == "":
            return []
        return val

from django.utils.safestring import mark_safe

@admin.register(Article)
class ArticleAdmin(ModelAdmin):
    form = ArticleAdminForm
    change_list_template = "admin/api/article/change_list.html"
    list_display = ('title', 'status_badge', 'published_at', 'category', 'edit_button', 'delete_button', 'index_page')
    
    @display(description="Status")
    def status_badge(self, obj):
        from django.utils import timezone
        if obj.status == 'draft':
            return mark_safe('<span style="background-color: #f1f5f9; color: #475569; padding: 3px 8px; border-radius: 6px; font-weight: bold; font-size: 11px;">Draft</span>')
        elif obj.is_published:
            return mark_safe('<span style="background-color: #ecfdf5; color: #059669; padding: 3px 8px; border-radius: 6px; font-weight: bold; font-size: 11px;">Published</span>')
        else:
            time_str = obj.published_at.strftime('%Y-%m-%d %H:%M') if obj.published_at else ''
            return format_html('<span style="background-color: #eff6ff; color: #2563eb; padding: 3px 8px; border-radius: 6px; font-weight: bold; font-size: 11px;" title="Scheduled for {}">Scheduled ({})</span>', time_str, time_str)

    @display(description="Edit")
    def edit_button(self, obj):
        url = reverse('admin:api_article_change', args=[obj.id])
        return format_html('<a href="{}" class="text-primary-600 hover:text-primary-800" title="Edit"><span class="material-symbols-outlined align-middle" style="font-size: 20px;">edit</span></a>', url)

    @display(description="Delete")
    def delete_button(self, obj):
        url = reverse('admin:api_article_delete', args=[obj.id])
        return format_html('<a href="{}" class="text-red-600 hover:text-red-800" title="Delete"><span class="material-symbols-outlined align-middle" style="font-size: 20px;">delete</span></a>', url)
    
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ('title', 'content')
    list_filter = ('status', 'category', 'published_at', 'index_page')
    fieldsets = (
        ('Publication & Schedule', {
            'fields': ('status', 'published_at'),
            'classes': ('collapse',),
            'description': 'Schedule when this article will be visible on the website. Articles with a future date/time or Draft status will stay hidden from public visitors until the scheduled time.'
        }),
        ('Content', {
            'fields': ('title', 'slug', 'excerpt', 'content', 'image', 'image_alt_text', 'author', 'category', 'category_color'),
            'classes': ('collapse',),
        }),
        ('Frequently Asked Questions (FAQs)', {
            'fields': ('faqs',),
            'classes': ('collapse',),
            'description': 'Add FAQ question and answer pairs for this article.'
        }),
        ('SEO & Metadata', {
            'fields': ('meta_title', 'meta_description', 'canonical_url', 'index_page', 'follow_links'),
            'classes': ('collapse',),
            'description': 'Control how search engines see this page.'
        }),
        ('Social Media (Open Graph)', {
            'fields': ('og_title', 'og_description', 'og_image'),
            'classes': ('collapse',),
        }),
        ('Schema Markup', {
            'fields': ('schema_type', 'schema_markup'),
            'classes': ('collapse',),
            'description': 'Advanced: Add structured data for rich snippets.'
        }),
    )

class SubServiceInline(TabularInline):
    model = SubService
    extra = 1
    prepopulated_fields = {'slug': ('title',)}
    fields = ('title', 'slug', 'description', 'index_page', 'follow_links')
    classes = ['collapse']

class SecondOpinionInline(StackedInline):
    model = SecondOpinion
    extra = 0
    fields = ('title', 'paragraph_1', 'paragraph_2', 'order', 'is_active')
    verbose_name = "Specialized Orthopedic Care (Second Opinion)"
    verbose_name_plural = "Specialized Orthopedic Care (Second Opinions)"
    classes = ['collapse']

@admin.register(Service)
class ServiceAdmin(ModelAdmin):
    form = ServiceAdminForm
    inlines = [SubServiceInline, SecondOpinionInline]
    change_list_template = "admin/api/service/change_list.html"
    list_display = ('title', 'edit_button', 'delete_button', 'updated_at', 'index_page')
    
    @display(description="Edit")
    def edit_button(self, obj):
        url = reverse('admin:api_service_change', args=[obj.id])
        return format_html('<a href="{}" class="text-primary-600 hover:text-primary-800" title="Edit"><span class="material-symbols-outlined align-middle" style="font-size: 20px;">edit</span></a>', url)

    @display(description="Delete")
    def delete_button(self, obj):
        url = reverse('admin:api_service_delete', args=[obj.id])
        return format_html('<a href="{}" class="text-red-600 hover:text-red-800" title="Delete"><span class="material-symbols-outlined align-middle" style="font-size: 20px;">delete</span></a>', url)

    prepopulated_fields = {'slug': ('title',)}
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'slug', 'description', 'icon', 'image', 'image_alt_text'),
            'classes': ('collapse',),
            'description': 'Configure core service details including title, URL slug, overview description, icon and featured image.'
        }),
        ('FAQ Section (Badge, Title, Subtitle & Q&A)', {
            'fields': ('faq_badge', 'faq_title', 'faq_description', 'faqs'),
            'classes': ('collapse',),
            'description': 'Configure FAQ badge, title, subtitle/description, and question/answer pairs for this specific service.'
        }),
        ('Treatment & Value Sections', {
            'fields': ('conditions_title', 'conditions', 'checklist_title', 'checklist_image', 'checklist_items', 'tag_badges'),
            'classes': ('collapse',),
            'description': 'Optional: Customize section headings, upload illustrations, or override conditions, checklist items, and tag badges.'
        }),
        ('Custom Detailed Sections (About, Indications & Commonly Treated)', {
            'fields': (
                'about_title', 'about_description',
                'who_needs_title', 'who_needs_description', 'who_needs_items',
                'commonly_treated_title', 'commonly_treated_description', 'commonly_treated'
            ),
            'classes': ('collapse',),
            'description': 'Optional: Customize detailed section content.'
        }),
        ('Highlight Section (Doctor Profile / Why Choose Us Extra)', {
            'fields': (
                'highlight_badge', 'highlight_title', 'highlight_description',
                'highlight_checklist_title', 'highlight_checklist_items',
                'highlight_doctor_image', 'highlight_doctor_name', 'highlight_doctor_role',
                'highlight_doctor_badges', 'highlight_doctor_description'
            ),
            'classes': ('collapse',),
            'description': 'Optional: Add a specialized highlight section (e.g. Why Choose Dr Ulhas) with a doctor profile card.'
        }),
        ('Journey Section (Step-by-step)', {
            'fields': (
                'journey_is_active', 'journey_title', 'journey_description', 'journey_steps'
            ),
            'classes': ('collapse',),
            'description': 'Optional: Add a step-by-step journey section (e.g. Your Robotic Knee Replacement Journey).'
        }),
        ('Second Opinion Section (Specialized Orthopedic Care)', {
            'fields': (
                'second_opinion_is_active', 'second_opinion_badge', 'second_opinion_title', 'second_opinion_description'
            ),
            'classes': ('collapse',),
            'description': 'Customize the Second Opinion / Specialized Orthopedic Care section heading and intro.'
        }),
        ('SEO & Social', {
            'fields': ('meta_title', 'meta_description', 'canonical_url', 'og_title', 'og_description', 'og_image', 'index_page', 'follow_links'),
            'classes': ('collapse',),
            'description': 'Control search engine indexing, metadata, and social preview cards.'
        }),
        ('Schema Markup', {
            'fields': ('schema_type', 'schema_markup'),
            'classes': ('collapse',),
            'description': 'Structured JSON-LD schema markup for rich Google search results.'
        }),
    )

@admin.register(SubService)
class SubServiceAdmin(ModelAdmin):
    list_display = ('title', 'service', 'slug', 'index_page', 'follow_links', 'created_at')
    list_editable = ('index_page', 'follow_links')
    list_filter = ('service', 'index_page', 'follow_links')
    search_fields = ('title', 'service__title')
    prepopulated_fields = {'slug': ('title',)}

    fieldsets = (
        ('Sub Service Information', {
            'fields': ('service', 'title', 'slug', 'description'),
            'classes': ('collapse',),
            'description': 'Configure parent service, title, URL slug and sub-service details.'
        }),
        ('Search Engine Indexing & Robots Directives', {
            'fields': ('index_page', 'follow_links'),
            'classes': ('collapse',),
            'description': 'Control search engine bot crawling (index/noindex, follow/nofollow) for this sub-service.'
        }),
    )

@admin.register(Translation)
class TranslationAdmin(ModelAdmin):
    list_display = ('key', 'language')
    list_filter = ('language',)
    search_fields = ('key', 'value')

@admin.register(SiteSetting)
class SiteSettingAdmin(ModelAdmin):
    def has_add_permission(self, request):
        # Only allow one instance of SiteSetting
        return not SiteSetting.objects.exists()

    fieldsets = (
        ('Robots.txt & Crawling Rules', {
            'fields': ('robots_txt',),
            'description': 'Configure search engine bot crawling rules.'
        }),
        ('Sitemap.xml Configuration', {
            'fields': ('sitemap_xml',),
            'description': 'Custom XML Sitemap rules. Leave empty to automatically generate dynamic sitemap from articles & services.'
        }),
        ('Global Scripts', {
            'fields': ('header_scripts', 'footer_scripts'),
            'description': 'Add GSC, GA4, or Facebook Pixel scripts here.'
        }),
        ('Internal Linking', {
            'fields': ('internal_linking_rules',),
            'classes': ('collapse',),
        }),
    )


@admin.register(HeroVideo)
class HeroVideoAdmin(ModelAdmin):
    list_display = ('__str__', 'updated_at')

    def has_add_permission(self, request):
        # Only allow one hero video object to exist
        return not HeroVideo.objects.exists()

@admin.register(CustomRedirect)
class CustomRedirectAdmin(ModelAdmin):
    list_display = ('old_path', 'new_path', 'status_code', 'created_at')
    list_filter = ('status_code',)
    search_fields = ('old_path', 'new_path')


@admin.register(GalleryItem)
class GalleryItemAdmin(ModelAdmin):
    change_list_template = "admin/api/galleryitem/change_list.html"
    list_display = ('title', 'edit_button', 'delete_button', 'category', 'span', 'order', 'created_at')
    list_filter = ('category',)
    search_fields = ('title', 'description')
    ordering = ('order', '-created_at')

    @display(description="Edit")
    def edit_button(self, obj):
        url = reverse('admin:api_galleryitem_change', args=[obj.id])
        return format_html('<a href="{}" class="text-primary-600 hover:text-primary-800" title="Edit"><span class="material-symbols-outlined align-middle" style="font-size: 20px;">edit</span></a>', url)

    @display(description="Delete")
    def delete_button(self, obj):
        url = reverse('admin:api_galleryitem_delete', args=[obj.id])
        return format_html('<a href="{}" class="text-red-600 hover:text-red-800" title="Delete"><span class="material-symbols-outlined align-middle" style="font-size: 20px;">delete</span></a>', url)


@admin.register(SecondOpinion)
class SecondOpinionAdmin(ModelAdmin):
    list_display = ('title', 'edit_button', 'delete_button', 'order', 'is_active', 'updated_at')
    list_filter = ('is_active',)
    search_fields = ('title', 'paragraph_1', 'paragraph_2')
    list_editable = ('order', 'is_active')
    ordering = ('order', 'created_at')

    @display(description="Edit")
    def edit_button(self, obj):
        url = reverse('admin:api_secondopinion_change', args=[obj.id])
        return format_html('<a href="{}" class="text-primary-600 hover:text-primary-800" title="Edit"><span class="material-symbols-outlined align-middle" style="font-size: 20px;">edit</span></a>', url)

    @display(description="Delete")
    def delete_button(self, obj):
        url = reverse('admin:api_secondopinion_delete', args=[obj.id])
        return format_html('<a href="{}" class="text-red-600 hover:text-red-800" title="Delete"><span class="material-symbols-outlined align-middle" style="font-size: 20px;">delete</span></a>', url)

    fieldsets = (
        ('Second Opinion Information', {
            'fields': ('title', 'category')
        }),
        ('Paragraph Content', {
            'fields': ('paragraph_1', 'paragraph_2'),
            'description': 'Paragraph 1: Basis of surgical decisions. Paragraph 2: What options a second opinion clarifies.'
        }),
        ('Ordering & Status', {
            'fields': ('order', 'is_active')
        }),
    )


class HomePageAdminForm(SEOBaseAdminForm):
    class Meta:
        model = HomePage
        fields = "__all__"
        widgets = {
            "hero_description": forms.Textarea(attrs={'rows': 3}),
            "hero_stats": HeroStatsWidget(),
            "faqs": FaqWidget(),
            "sports_items": SportsInjuryItemsWidget(),
            "trust_cards": TrustCardsWidget(),
        }


@admin.register(HomePage)
class HomePageAdmin(ModelAdmin):
    form = HomePageAdminForm
    list_display = ('title', 'hero_headline_1', 'trust_badge', 'sports_badge', 'meta_title', 'updated_at')

    def has_add_permission(self, request):
        return not HomePage.objects.exists()

    fieldsets = (
        ('General', {
            'fields': ('title',)
        }),
        ('Hero Section (Main Banner, Headlines, Buttons & Doctor Card)', {
            'fields': (
                'hero_is_active',
                'hero_badge',
                'hero_headline_1',
                'hero_headline_2',
                'hero_headline_3',
                'hero_description',
                'hero_book_btn_text',
                'hero_book_btn_link',
                'hero_report_btn_text',
                'hero_report_btn_link',
                'hero_services_btn_text',
                'hero_services_btn_link',
                'hero_doctor_name',
                'hero_doctor_role',
                'hero_video_file',
                'hero_video_url',
                'hero_stats',
            ),
            'description': 'Configure the main hero banner headlines, CTA buttons, Doctor card details, video, and live animated stats row.'
        }),
        ('Why Patients Trust Section (Patient-Focused Excellence)', {
            'fields': (
                'trust_is_active',
                'trust_badge',
                'trust_title',
                'trust_title_highlight',
                'trust_description',
                'trust_cards',
            ),
            'classes': ('collapse',),
            'description': 'Configure the Patient-Focused Excellence section (heading, subtext, and feature cards).'
        }),
        ('Sports Injury Clinic Section', {
            'fields': (
                'sports_is_active',
                'sports_badge',
                'sports_title',
                'sports_title_highlight',
                'sports_title_end',
                'sports_description',
                'sports_video_embed_url',
                'sports_video_file',
                'sports_dashboard_label',
                'sports_learn_more_heading',
                'sports_items',
                'sports_cta_text',
                'sports_cta_link',
            ),
            'classes': ('collapse',),
            'description': 'Configure the Sports Injury Clinic Section shown on the Home page (video reel/upload and dynamic treatment points).'
        }),
        ('FAQ Section (Badge, Title, Subtitle & Q&A)', {
            'fields': ('faq_badge', 'faq_title', 'faq_description', 'faqs'),
            'description': 'Configure the FAQ section shown on the Home page (Badge, Heading, Subtitle/Description, and interactive Questions/Answers).'
        }),
        ('SEO & Metadata', {
            'fields': ('meta_title', 'meta_description', 'canonical_url', 'index_page', 'follow_links', 'h1_title'),
            'classes': ('collapse',),
            'description': 'Control how search engines index and rank the Home Page.'
        }),
        ('Social Media (Open Graph)', {
            'fields': ('og_title', 'og_description', 'og_image'),
            'classes': ('collapse',),
            'description': 'Control preview cards on Facebook, WhatsApp, LinkedIn, etc.'
        }),
        ('Schema Markup', {
            'fields': ('schema_type', 'schema_markup'),
            'classes': ('collapse',),
            'description': 'Structured JSON-LD schema markup for rich Google search results.'
        }),
    )


class SportingInjurySectionAdminForm(forms.ModelForm):
    class Meta:
        model = SportingInjurySection
        fields = "__all__"
        widgets = {
            "items": SportsInjuryItemsWidget(),
        }


@admin.register(SportingInjurySection)
class SportingInjurySectionAdmin(ModelAdmin):
    form = SportingInjurySectionAdminForm
    list_display = ('title', 'title_highlight', 'dashboard_label', 'is_active', 'updated_at')

    def has_add_permission(self, request):
        return not SportingInjurySection.objects.exists()

    fieldsets = (
        ('Section Headings & Description', {
            'fields': ('badge', 'title', 'title_highlight', 'title_end', 'description'),
            'description': 'Customize the main headings and introduction for the Sports Injury Clinic section.'
        }),
        ('Video & Media Reel', {
            'fields': ('video_embed_url', 'video_file', 'dashboard_label'),
            'description': 'Configure the Instagram Reel / YouTube embed URL or upload a direct video file, along with the card label.'
        }),
        ('Features & Treatments (List)', {
            'fields': ('learn_more_heading', 'items'),
            'description': 'Interactive management of treatment and recovery bullet points.'
        }),
        ('Call To Action & Status', {
            'fields': ('cta_text', 'cta_link', 'is_active'),
        }),
    )


class ServicesPageAdminForm(SEOBaseAdminForm):
    class Meta:
        model = ServicesPage
        fields = "__all__"
        widgets = {
            "faqs": FaqWidget(),
        }


@admin.register(ServicesPage)
class ServicesPageAdmin(ModelAdmin):
    form = ServicesPageAdminForm
    list_display = ('title', 'faq_title', 'meta_title', 'updated_at')

    def has_add_permission(self, request):
        return not ServicesPage.objects.exists()

    fieldsets = (
        ('General', {
            'fields': ('title',)
        }),
        ('FAQ Section (Badge, Title, Subtitle & Q&A)', {
            'fields': ('faq_badge', 'faq_title', 'faq_description', 'faqs'),
            'description': 'Configure the FAQ section shown on the Services page (Badge, Heading, Subtitle/Description, and interactive Questions/Answers).'
        }),
        ('SEO & Metadata', {
            'fields': ('meta_title', 'meta_description', 'canonical_url', 'index_page', 'follow_links', 'h1_title'),
            'classes': ('collapse',),
            'description': 'Control how search engines index and rank the Services Page.'
        }),
        ('Social Media (Open Graph)', {
            'fields': ('og_title', 'og_description', 'og_image'),
            'classes': ('collapse',),
            'description': 'Control preview cards on Facebook, WhatsApp, LinkedIn, etc.'
        }),
        ('Schema Markup', {
            'fields': ('schema_type', 'schema_markup'),
            'classes': ('collapse',),
            'description': 'Structured JSON-LD schema markup for rich Google search results.'
        }),
    )






