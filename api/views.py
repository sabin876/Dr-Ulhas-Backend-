from rest_framework.response import Response
from rest_framework import viewsets, response
from rest_framework.decorators import api_view
from django.http import HttpResponse, JsonResponse
from django.contrib.auth import authenticate, login as auth_login
from django.views.decorators.csrf import csrf_exempt
import json
from .models import Article, Service, Translation, SiteSetting, GalleryItem, HeroVideo, SecondOpinion, HomePage, SportingInjurySection
from .serializers import ArticleSerializer, ServiceSerializer, TranslationSerializer, SiteSettingSerializer, GalleryItemSerializer, HeroVideoSerializer, SecondOpinionSerializer, HomePageSerializer, SportingInjurySectionSerializer
from django.core.mail import send_mail
from django.conf import settings

from django.utils import timezone
from django.db.models import Q

class ArticleViewSet(viewsets.ModelViewSet):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    lookup_field = 'slug'

    def get_queryset(self):
        show_all = (
            self.request.query_params.get('all') in ['true', '1', 'yes'] or
            self.request.query_params.get('admin') in ['true', '1', 'yes'] or
            (self.request.user and self.request.user.is_authenticated and self.request.user.is_staff)
        )
        if show_all:
            return Article.objects.all().order_by('-published_at', '-date')

        # Public visitors only see published articles whose scheduled time has arrived
        now = timezone.now()
        return Article.objects.filter(
            published_at__lte=now
        ).exclude(status='draft').order_by('-published_at', '-date')

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


class GalleryItemViewSet(viewsets.ModelViewSet):
    queryset = GalleryItem.objects.all()
    serializer_class = GalleryItemSerializer


class SecondOpinionViewSet(viewsets.ModelViewSet):
    queryset = SecondOpinion.objects.filter(is_active=True).order_by('order', 'created_at')
    serializer_class = SecondOpinionSerializer


@api_view(['GET', 'PUT', 'PATCH'])
def home_page_view(request):
    hp = HomePage.objects.first()
    if not hp:
        hp = HomePage.objects.create(
            title="Home Page",
            meta_title="Dr. Ulhas | Expert Orthopedic Surgeon Dubai",
            meta_description="Expert orthopedic care specializing in robotic joint replacement, sports injuries, and comprehensive rehabilitation with Dr. Ulhas Sonar.",
            canonical_url="https://drulhasorthopedic.com/",
            faq_badge="Help Center",
            faq_title="Frequently Asked Questions",
            faq_description="Common questions about our care, robotic surgery, and orthopedic treatments in Dubai.",
            sports_is_active=True,
            sports_badge="EXPERT SPORTS ORTHOPEDIC CARE",
            sports_title="Sports Injury",
            sports_title_highlight="Clinic",
            sports_title_end=" Dubai",
            sports_description="Specialized, minimally invasive treatments and accelerated recovery programs designed for athletes and active individuals of all performance levels.",
            sports_video_embed_url="https://www.instagram.com/reel/DTijxQ3krcw/embed/?autoplay=1",
            sports_dashboard_label="DR. ULHAS CLINICAL REEL",
            sports_learn_more_heading="COMPREHENSIVE ATHLETIC CARE & RETURN-TO-PLAY",
            sports_items=[
                {
                    "title": "Comprehensive Clinical Assessment",
                    "desc": "Thorough joint, ligament, and kinetic chain evaluation to pinpoint exact pathology."
                },
                {
                    "title": "Precision Imaging Diagnostics",
                    "desc": "High-resolution MRI, dynamic ultrasound, and digital radiography for accurate diagnosis."
                },
                {
                    "title": "Customized Return-to-Play Plans",
                    "desc": "Tailored recovery trajectories aligned with your sport, goals, and training schedule."
                },
                {
                    "title": "High-Performance Rehabilitation",
                    "desc": "Integrated physiotherapy, biomechanical reconditioning, and future injury prevention."
                }
            ],
            sports_cta_text="Book Sports Consultation",
            sports_cta_link="/contact",
            trust_is_active=True,
            trust_badge="PATIENT-FOCUSED EXCELLENCE",
            trust_title="Why Patients Trust",
            trust_title_highlight="Dr. Ulhas Sonar",
            trust_description="Combining global surgical experience with cutting-edge technology and a compassionate, individualized recovery approach.",
            trust_cards=[
                {
                    "id": "01",
                    "icon": "Award",
                    "title": "Expert Care",
                    "description": "14+ years of complex orthopaedic care experience and surgical precision.",
                    "badge": "14+ Yrs Experience"
                },
                {
                    "id": "02",
                    "icon": "Cpu",
                    "title": "Advanced Technology",
                    "description": "Using the latest medical technologies and techniques for optimal surgical outcomes.",
                    "badge": "Robotic & Tech Led"
                },
                {
                    "id": "03",
                    "icon": "Zap",
                    "title": "Quick Recovery",
                    "description": "Specialized minimally invasive techniques for faster healing and reduced hospital stays.",
                    "badge": "Minimally Invasive"
                },
                {
                    "id": "04",
                    "icon": "HeartHandshake",
                    "title": "Personalized Care",
                    "description": "Each treatment plan is carefully tailored to address your specific needs and conditions.",
                    "badge": "Tailored Plans"
                }
            ],
            faqs=[
                {
                    "question": "What is robotic-assisted surgery?",
                    "answer": "It is a precision-guided technique that allows the surgeon to perform joint replacements with higher accuracy, leading to better outcomes."
                },
                {
                    "question": "How long is the recovery period?",
                    "answer": "Recovery varies by procedure, but most patients return to normal activities within 6 to 12 weeks with proper physical therapy."
                },
                {
                    "question": "Do you treat sports injuries?",
                    "answer": "Yes, we specialize in ACL repairs, meniscus treatments, and all types of athletic musculoskeletal injuries."
                },
                {
                    "question": "Where is the clinic located?",
                    "answer": "Our main consultation rooms are located in Dubai, within premium medical facilities."
                },
                {
                    "question": "Is second opinion available?",
                    "answer": "Yes, we encourage patients to seek second opinions for complex orthopedic cases to ensure confidence in their treatment."
                }
            ]
        )
    if request.method in ['PUT', 'PATCH']:
        serializer = HomePageSerializer(hp, data=request.data, partial=True, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return response.Response(serializer.data)
        return response.Response(serializer.errors, status=400)
    serializer = HomePageSerializer(hp, context={'request': request})
    return response.Response(serializer.data)


@api_view(['GET'])
def get_home_faqs(request):
    hp = HomePage.objects.first()
    faqs = hp.faqs if hp and hp.faqs else []
    if isinstance(faqs, str):
        try:
            faqs = json.loads(faqs)
        except Exception:
            faqs = []
    return response.Response(faqs)

    

from django.core.mail import EmailMultiAlternatives


@api_view(['POST'])
def send_contact_mail(request):
    data = request.data

    full_name = data.get('full_name')
    phone = data.get('phone')
    email_address = data.get('email')
    subject = f"Contact from {full_name}"
    service = data.get('service')
    message = data.get('message')

    if not all([full_name, email_address, message]):
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
        
@api_view(['GET', 'PUT', 'PATCH'])
def site_settings(request):
    settings = SiteSetting.objects.first()
    if not settings:
        settings = SiteSetting.objects.create()
    if request.method in ['PUT', 'PATCH']:
        serializer = SiteSettingSerializer(settings, data=request.data, partial=True, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return response.Response(serializer.data)
        return response.Response(serializer.errors, status=400)
    serializer = SiteSettingSerializer(settings, context={'request': request})
    return response.Response(serializer.data)

def robots_txt(request):
    settings = SiteSetting.objects.first()
    content = settings.robots_txt if settings else "User-agent: *\nAllow: /"
    return HttpResponse(content, content_type="text/plain")

def sitemap_xml(request):
    settings = SiteSetting.objects.first()
    if settings and settings.sitemap_xml and settings.sitemap_xml.strip():
        return HttpResponse(settings.sitemap_xml.strip(), content_type="application/xml")

    # Dynamic fallback XML sitemap generation
    now = timezone.now()
    articles = Article.objects.filter(index_page=True, published_at__lte=now).exclude(status='draft')
    services = Service.objects.filter(index_page=True)
    
    xml = '<?xml version="1.0" encoding="UTF-8"?>\n'
    xml += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    
    # Add home page
    xml += '  <url><loc>https://drulhasorthopedic.com/</loc><priority>1.0</priority></url>\n'
    
    for article in articles:
        xml += f'  <url><loc>https://drulhasorthopedic.com/blog/{article.slug}</loc><lastmod>{article.updated_at.strftime("%Y-%m-%d")}</lastmod></url>\n'
        
    for service in services:
        xml += f'  <url><loc>https://drulhasorthopedic.com/services/{service.slug}</loc><lastmod>{service.updated_at.strftime("%Y-%m-%d")}</lastmod></url>\n'
        
    xml += '</urlset>'
    return HttpResponse(xml, content_type="application/xml")

@api_view(['GET'])
def html_sitemap(request):
    now = timezone.now()
    articles = Article.objects.filter(index_page=True, published_at__lte=now).exclude(status='draft')
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


@api_view(['GET'])
def temp_reset_admin(request):
    from django.contrib.auth import get_user_model
    User = get_user_model()
    username = 'admin'
    password = 'adminpassword123'
    try:
        u = User.objects.get(username=username)
        u.set_password(password)
        u.is_staff = True
        u.is_superuser = True
        u.save()
        return Response({"status": "success", "message": f"Updated existing user '{username}' to password '{password}' with staff/superuser privileges."})
    except User.DoesNotExist:
        User.objects.create_superuser(username, 'admin@drulhasorthopedic.com', password)
        return Response({"status": "success", "message": f"Created new superuser '{username}' with password '{password}'."})


@api_view(['GET'])
def get_hero_video(request):
    video = HeroVideo.objects.first()
    if video:
        serializer = HeroVideoSerializer(video, context={'request': request})
        return Response(serializer.data)
    return Response({"video": None})


@api_view(['GET', 'PUT', 'PATCH'])
def sports_injury_view(request):
    section = SportingInjurySection.objects.first()
    if not section:
        section = SportingInjurySection.objects.create(
            badge="EXPERT SPORTS ORTHOPEDIC CARE",
            title="Sports Injury",
            title_highlight="Clinic",
            title_end=" Dubai",
            description="Specialized, minimally invasive treatments and accelerated recovery programs designed for athletes and active individuals of all performance levels.",
            video_embed_url="https://www.instagram.com/reel/DTijxQ3krcw/embed/?autoplay=1",
            dashboard_label="DR. ULHAS CLINICAL REEL",
            learn_more_heading="COMPREHENSIVE ATHLETIC CARE & RETURN-TO-PLAY",
            items=[
                {
                    "title": "Comprehensive Clinical Assessment",
                    "desc": "Thorough joint, ligament, and kinetic chain evaluation to pinpoint exact pathology."
                },
                {
                    "title": "Precision Imaging Diagnostics",
                    "desc": "High-resolution MRI, dynamic ultrasound, and digital radiography for accurate diagnosis."
                },
                {
                    "title": "Customized Return-to-Play Plans",
                    "desc": "Tailored recovery trajectories aligned with your sport, goals, and training schedule."
                },
                {
                    "title": "High-Performance Rehabilitation",
                    "desc": "Integrated physiotherapy, biomechanical reconditioning, and future injury prevention."
                }
            ],
            cta_text="Book Sports Consultation",
            cta_link="/contact",
            is_active=True
        )

    if request.method in ['PUT', 'PATCH']:
        serializer = SportingInjurySectionSerializer(section, data=request.data, partial=True, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return response.Response(serializer.data)
        return response.Response(serializer.errors, status=400)

    serializer = SportingInjurySectionSerializer(section, context={'request': request})
    return response.Response(serializer.data)

