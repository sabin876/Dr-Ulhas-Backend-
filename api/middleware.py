from django.utils.deprecation import MiddlewareMixin
from .models import CustomRedirect
from django.http import HttpResponseRedirect, HttpResponsePermanentRedirect, HttpResponse

class SEOMiddleware(MiddlewareMixin):
    def process_request(self, request):
        # 1. Custom Redirect Management
        path = request.path
        try:
            redirect = CustomRedirect.objects.get(old_path=path)
            if redirect.status_code == 301:
                return HttpResponsePermanentRedirect(redirect.new_path)
            elif redirect.status_code == 302:
                return HttpResponseRedirect(redirect.new_path)
            elif redirect.status_code == 410:
                return HttpResponse("410 Gone", status=410)
            elif redirect.status_code == 451:
                return HttpResponse("451 Unavailable for Legal Reasons", status=451)
        except CustomRedirect.DoesNotExist:
            pass
        return None

    def process_response(self, request, response):
        # 2. X-Robots-Tag Injection
        # This is simplified. Ideally, we'd check if the view is associated with a model that has index/follow fields.
        # For now, we can inject a default or check if it's set in the context.
        if hasattr(request, 'seo_noindex') and request.seo_noindex:
            response['X-Robots-Tag'] = 'noindex, nofollow'
        
        # 3. Security Headers (Optional but good for CMS)
        response['X-Content-Type-Options'] = 'nosniff'
        response['X-Frame-Options'] = 'DENY'
        
        return response
