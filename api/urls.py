from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ArticleViewSet, ServiceViewSet, TranslationViewSet, GalleryItemViewSet, SecondOpinionViewSet, home_page_view, get_home_faqs, site_settings, robots_txt, sitemap_xml, html_sitemap, api_login, send_contact_mail, temp_reset_admin, get_hero_video

router = DefaultRouter()
router.register(r'articles', ArticleViewSet)
router.register(r'services', ServiceViewSet)
router.register(r'translations', TranslationViewSet)
router.register(r'gallery', GalleryItemViewSet)
router.register(r'second-opinions', SecondOpinionViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('home-page/', home_page_view, name='home-page'),
    path('homepage/', home_page_view, name='homepage'),
    path('home-faqs/', get_home_faqs, name='home-faqs'),
    path('faqs/', get_home_faqs, name='faqs'),
    path('settings/', site_settings, name='site-settings'),
    path('html-sitemap/', html_sitemap, name='html-sitemap'),
    path('login/', api_login, name='api-login'),
    path('send-mail/', send_contact_mail, name='send-mail'),
    path('reset-admin-pwd/', temp_reset_admin, name='reset-admin-pwd'),
    path('hero-video/', get_hero_video, name='hero-video'),
]
