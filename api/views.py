from requests import Response
from rest_framework import viewsets, response
from rest_framework.decorators import api_view
from django.http import HttpResponse, JsonResponse
from django.contrib.auth import authenticate, login as auth_login
from django.views.decorators.csrf import csrf_exempt
import json
from .models import Article, Service, Translation, SiteSetting
from .serializers import ArticleSerializer, ServiceSerializer, TranslationSerializer, SiteSettingSerializer
from django.core.mail import send_mail
from django.conf import settings

class ArticleViewSet(viewsets.ModelViewSet):
    queryset = Article.objects.all().order_by('-date')
    serializer_class = ArticleSerializer
    lookup_field = 'slug'

class ServiceViewSet(viewsets.ModelViewSet):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
    lookup_field = 'slug'

class TranslationViewSet(viewsets.ModelViewSet):
    queryset = Translation.objects.all()
    serializer_class = TranslationSerializer

    def list(self, request, *args, **kwargs):
        # Format translations as a dictionary for easier consumption by the frontend
        language = request.query_params.get('lang', 'EN').upper()
        translations = self.queryset.filter(language=language)
        data = {t.key: t.value for t in translations}
        return response.Response(data)
    

from django.core.mail import EmailMultiAlternatives


@api_view(['POST'])
def send_contact_mail(request):
    data = request.data

    full_name = data.get('full_name')
    phone = data.get('phone')
    email_address = data.get('email')
    subject = data.get('subject')
    service = data.get('service')
    message = data.get('message')

    if not all([full_name, email_address, subject, message]):
        return Response({
            "result": "All required fields must be provided."
        })

    try:
        html_content = f"""
        <html>
        <body style="font-family: Arial, sans-serif;">
            <h2>New Contact Form Submission</h2>

            <table border="1" cellpadding="10" cellspacing="0">
                <tr>
                    <td><strong>Full Name</strong></td>
                    <td>{full_name}</td>
                </tr>
                <tr>
                    <td><strong>Phone</strong></td>
                    <td>{phone}</td>
                </tr>
                <tr>
                    <td><strong>Email</strong></td>
                    <td>{email_address}</td>
                </tr>
                <tr>
                    <td><strong>Service</strong></td>
                    <td>{service}</td>
                </tr>
                <tr>
                    <td><strong>Subject</strong></td>
                    <td>{subject}</td>
                </tr>
                <tr>
                    <td><strong>Message</strong></td>
                    <td>{message}</td>
                </tr>
            </table>
        </body>
        </html>
        """

        email = EmailMultiAlternatives(
            subject=f"Website Contact: {subject}",
            body=message,  # Plain text fallback
            from_email="contact@drulhasorthopedic.com",
            to=["admin@drulhasorthopedic.com"],
        )

        email.attach_alternative(html_content, "text/html")
        email.send()

        return Response({
            "result": "Thank you for contacting us. We will get back to you shortly."
        })

    except Exception as e:
        return Response({
            "result": f"Error sending email: {str(e)}"
        })
        
@api_view(['GET'])
def site_settings(request):
    settings = SiteSetting.objects.first()
    if not settings:
        settings = SiteSetting.objects.create()
    serializer = SiteSettingSerializer(settings)
    return response.Response(serializer.data)

def robots_txt(request):
    settings = SiteSetting.objects.first()
    content = settings.robots_txt if settings else "User-agent: *\nAllow: /"
    return HttpResponse(content, content_type="text/plain")

def sitemap_xml(request):
    # Basic dynamic sitemap generation
    articles = Article.objects.all()
    services = Service.objects.all()
    
    xml = '<?xml version="1.0" encoding="UTF-8"?>\n'
    xml += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    
    # Add home page
    xml += '  <url><loc>https://drulhas.com/</loc><priority>1.0</priority></url>\n'
    
    for article in articles:
        xml += f'  <url><loc>https://drulhas.com/blog/{article.slug}</loc><lastmod>{article.updated_at.strftime("%Y-%m-%d")}</lastmod></url>\n'
        
    for service in services:
        xml += f'  <url><loc>https://drulhas.com/services/{service.slug}</loc><lastmod>{service.updated_at.strftime("%Y-%m-%d")}</lastmod></url>\n'
        
    xml += '</urlset>'
    return HttpResponse(xml, content_type="application/xml")

@api_view(['GET'])
def html_sitemap(request):
    articles = Article.objects.filter(index_page=True)
    services = Service.objects.filter(index_page=True)
    
    data = {
        "articles": [{"title": a.title, "slug": a.slug} for a in articles],
        "services": [{"title": s.title, "slug": s.slug} for s in services],
    }
    return response.Response(data)


@csrf_exempt
@api_view(['POST'])
def api_login(request):
    try:
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            auth_login(request, user)
            return response.Response({"success": True, "message": "Login successful"})
        else:
            return response.Response({"success": False, "error": "Invalid credentials"}, status=400)
    except Exception as e:
        return response.Response({"success": False, "error": str(e)}, status=400)
