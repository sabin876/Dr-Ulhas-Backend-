from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ArticleViewSet, ServiceViewSet, TranslationViewSet, site_settings, robots_txt, sitemap_xml, html_sitemap, api_login

router = DefaultRouter()
router.register(r'articles', ArticleViewSet)
router.register(r'services', ServiceViewSet)
router.register(r'translations', TranslationViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('settings/', site_settings, name='site-settings'),
    path('robots.txt', robots_txt, name='robots-txt'),
    path('sitemap.xml', sitemap_xml, name='sitemap-xml'),
    path('html-sitemap/', html_sitemap, name='html-sitemap'),
    path('login/', api_login, name='api-login'),
]
