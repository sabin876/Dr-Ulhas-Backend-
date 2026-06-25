from api.models import Article, Service, GalleryItem
from Report.models import Report

def dashboard_callback(request, context):
    context.update({
        "article_count": Article.objects.count(),
        "service_count": Service.objects.count(),
        "gallery_count": GalleryItem.objects.count(),
        "report_count": Report.objects.count(),
    })
    return context
