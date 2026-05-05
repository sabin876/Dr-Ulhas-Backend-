from django.contrib import admin
from .models import Article, Service, Translation, SiteSetting, CustomRedirect

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'date', 'category', 'index_page')
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ('title', 'content')
    list_filter = ('category', 'date', 'index_page')
    
    fieldsets = (
        ('Content', {
            'fields': ('title', 'h1_title', 'slug', 'excerpt', 'content', 'image', 'image_alt_text', 'author', 'category', 'category_color')
        }),
        ('SEO Configuration', {
            'fields': ('meta_title', 'meta_description', 'canonical_url', 'index_page', 'follow_links'),
            'classes': ('collapse',),
        }),
        ('Social Media (OG)', {
            'fields': ('og_title', 'og_description', 'og_image'),
            'classes': ('collapse',),
        }),
        ('Advanced SEO', {
            'fields': ('schema_markup',),
            'classes': ('collapse',),
        }),
    )

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('title', 'updated_at')
    prepopulated_fields = {'slug': ('title',)}
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'h1_title', 'slug', 'description', 'icon', 'image_alt_text', 'items')
        }),
        ('SEO', {
            'fields': ('meta_title', 'meta_description', 'canonical_url', 'og_title', 'og_description', 'og_image', 'schema_markup', 'index_page', 'follow_links'),
            'classes': ('collapse',),
        }),
    )

@admin.register(Translation)
class TranslationAdmin(admin.ModelAdmin):
    list_display = ('key', 'language')
    list_filter = ('language',)
    search_fields = ('key', 'value')

@admin.register(SiteSetting)
class SiteSettingAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        # Only allow one instance of SiteSetting
        return not SiteSetting.objects.exists()

    fieldsets = (
        ('Technical SEO', {
            'fields': ('robots_txt',)
        }),
        ('Global Scripts', {
            'fields': ('header_scripts', 'footer_scripts'),
            'help_text': 'Add GSC, GA4, or Facebook Pixel scripts here.'
        }),
        ('Internal Linking', {
            'fields': ('internal_linking_rules',),
            'classes': ('collapse',),
        }),
    )

@admin.register(CustomRedirect)
class CustomRedirectAdmin(admin.ModelAdmin):
    list_display = ('old_path', 'new_path', 'status_code', 'created_at')
    list_filter = ('status_code',)
    search_fields = ('old_path', 'new_path')
