"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.sitemaps.views import sitemap
from api.sitemaps import ArticleSitemap, ServiceSitemap, StaticViewSitemap

sitemaps = {
    'articles': ArticleSitemap,
    'services': ServiceSitemap,
    'static': StaticViewSitemap,
}

from api.views import robots_txt, sitemap_xml

from django.urls import re_path
from django.views.static import serve

from django.http import JsonResponse

def home_view(request):
    return JsonResponse({
        "status": "online",
        "message": "Dr. Ulhas Backend API is running successfully.",
        "frontend_url": "http://localhost:5173",
        "endpoints": {
            "admin": "/admin/",
            "api_articles": "/api/articles/",
            "api_services": "/api/services/",
            "api_settings": "/api/settings/",
        }
    })

urlpatterns = [
    path('', home_view, name='home'),
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
    path('api/', include('Report.urls')),
    path('sitemap.xml', sitemap_xml, name='sitemap-xml'),
    path('robots.txt', robots_txt, name='robots-txt'),
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
    re_path(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT}),
]

