from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ArticleViewSet, ServiceViewSet, TranslationViewSet, GalleryItemViewSet, site_settings, robots_txt, sitemap_xml, html_sitemap, api_login, send_contact_mail

router = DefaultRouter()
router.register(r'articles', ArticleViewSet)
router.register(r'services', ServiceViewSet)
router.register(r'translations', TranslationViewSet)
router.register(r'gallery', GalleryItemViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('settings/', site_settings, name='site-settings'),
    path('html-sitemap/', html_sitemap, name='html-sitemap'),
    path('login/', api_login, name='api-login'),
    path('send-mail/', send_contact_mail, name='send-mail'),
]
