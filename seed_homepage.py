import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from api.models import HomePage

initial_faqs = [
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

hp = HomePage.objects.first()
if not hp:
    hp = HomePage.objects.create(
        title="Home Page",
        meta_title="Dr. Ulhas | Expert Orthopedic Surgeon Dubai",
        meta_description="Expert orthopedic care specializing in robotic joint replacement, sports injuries, and comprehensive rehabilitation with Dr. Ulhas Sonar.",
        canonical_url="https://drulhasorthopedic.com/",
        og_title="Dr. Ulhas Sonar | Orthopaedic Surgeon Dubai",
        og_description="Expert orthopedic care specializing in joint replacement, sports injuries, and comprehensive rehabilitation with Dr. Ulhas.",
        faq_badge="Help Center",
        faq_title="Frequently Asked Questions",
        faq_description="Common questions about our care, robotic surgery, and orthopedic treatments in Dubai.",
        faqs=initial_faqs,
        index_page=True,
        follow_links=True
    )
    print("Created new Home Page configuration!")
else:
    hp.meta_title = hp.meta_title or "Dr. Ulhas | Expert Orthopedic Surgeon Dubai"
    hp.meta_description = hp.meta_description or "Expert orthopedic care specializing in robotic joint replacement, sports injuries, and comprehensive rehabilitation with Dr. Ulhas Sonar."
    hp.canonical_url = hp.canonical_url or "https://drulhasorthopedic.com/"
    hp.faqs = hp.faqs or initial_faqs
    hp.save()
    print("Updated existing Home Page configuration!")

print(f"Home Page Title: {hp.title}")
print(f"Meta Title: {hp.meta_title}")
print(f"Meta Description: {hp.meta_description}")
print(f"FAQs count: {len(hp.faqs)}")
