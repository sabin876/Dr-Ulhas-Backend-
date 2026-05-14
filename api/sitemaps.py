from django.contrib.sitemaps import Sitemap
from .models import Article, Service
from django.urls import reverse

class ArticleSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.8

    def items(self):
        return Article.objects.filter(index_page=True)

    def lastmod(self, obj):
        return obj.updated_at

    def location(self, obj):
        return f"/blog/{obj.slug}"

class ServiceSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.9

    def items(self):
        return Service.objects.filter(index_page=True)

    def lastmod(self, obj):
        return obj.updated_at

    def location(self, obj):
        return f"/services/{obj.slug}"

class StaticViewSitemap(Sitemap):
    priority = 1.0
    changefreq = 'daily'

    def items(self):
        return ['/', '/about', '/contact', '/gallery']

    def location(self, item):
        return item
