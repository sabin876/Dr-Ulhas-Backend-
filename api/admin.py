from unfold.admin import ModelAdmin
from unfold.decorators import display
from django.contrib import admin
from django import forms
from django.utils.html import format_html
from django.urls import reverse
from ckeditor.widgets import CKEditorWidget
from .models import Article, Service, Translation, SiteSetting, CustomRedirect, GalleryItem, HeroVideo
from django.contrib.auth.models import Group, User

try:
    admin.site.unregister(Group)
    admin.site.unregister(User)
except admin.sites.NotRegistered:
    pass

class ArticleAdminForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = "__all__"
        widgets = {
            "content": CKEditorWidget(),
        }

from .widgets import ListStringWidget, ConditionsWidget, CommonlyTreatedWidget

class ServiceAdminForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = "__all__"
        widgets = {
            "description": CKEditorWidget(),
            "about_description": CKEditorWidget(),
            "items": ListStringWidget(),
            "conditions": ConditionsWidget(),
            "checklist_items": ListStringWidget(),
            "tag_badges": ListStringWidget(),
            "who_needs_items": ListStringWidget(),
            "commonly_treated": CommonlyTreatedWidget(),
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

@admin.register(Article)
class ArticleAdmin(ModelAdmin):
    form = ArticleAdminForm
    change_list_template = "admin/api/article/change_list.html"
    list_display = ('title', 'edit_button', 'delete_button', 'date', 'category', 'index_page')
    
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
    list_filter = ('category', 'date', 'index_page')
    fieldsets = (
        ('Content', {
            'fields': ('title', 'slug', 'excerpt', 'content', 'image', 'image_alt_text', 'author', 'category', 'category_color')
        }),
        ('SEO & Metadata', {
            'fields': ('meta_title', 'meta_description', 'canonical_url', 'index_page', 'follow_links'),
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

@admin.register(Service)
class ServiceAdmin(ModelAdmin):
    form = ServiceAdminForm
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
            'fields': ('title', 'slug', 'description', 'icon', 'image', 'image_alt_text', 'items', 'faqs')
        }),
        ('Treatment & Value Sections', {
            'fields': ('conditions_title', 'conditions', 'checklist_title', 'checklist_image', 'checklist_items', 'tag_badges'),
            'description': 'Optional: Customize section headings, upload illustrations, or override conditions, checklist items, and tag badges.'
        }),
        ('Custom Detailed Sections (About, Indications & Commonly Treated)', {
            'fields': (
                'about_title', 'about_description',
                'who_needs_title', 'who_needs_description', 'who_needs_items',
                'commonly_treated_title', 'commonly_treated_description', 'commonly_treated'
            ),
            'description': 'Optional: Customize detailed section content.'
        }),
        ('SEO & Social', {
            'fields': ('meta_title', 'meta_description', 'canonical_url', 'og_title', 'og_description', 'og_image', 'index_page', 'follow_links'),
            'classes': ('collapse',),
        }),
        ('Schema Markup', {
            'fields': ('schema_type', 'schema_markup'),
            'classes': ('collapse',),
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
        ('Technical SEO', {
            'fields': ('robots_txt',)
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

