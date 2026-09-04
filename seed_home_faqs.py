import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from api.models import HomeFAQ

initial_faqs = [
    {
        "question": "What is robotic-assisted surgery?",
        "answer": "It is a precision-guided technique that allows the surgeon to perform joint replacements with higher accuracy, leading to better outcomes.",
        "order": 1,
        "is_active": True
    },
    {
        "question": "How long is the recovery period?",
        "answer": "Recovery varies by procedure, but most patients return to normal activities within 6 to 12 weeks with proper physical therapy.",
        "order": 2,
        "is_active": True
    },
    {
        "question": "Do you treat sports injuries?",
        "answer": "Yes, we specialize in ACL repairs, meniscus treatments, and all types of athletic musculoskeletal injuries.",
        "order": 3,
        "is_active": True
    },
    {
        "question": "Where is the clinic located?",
        "answer": "Our main consultation rooms are located in Dubai, within premium medical facilities.",
        "order": 4,
        "is_active": True
    },
    {
        "question": "Is second opinion available?",
        "answer": "Yes, we encourage patients to seek second opinions for complex orthopedic cases to ensure confidence in their treatment.",
        "order": 5,
        "is_active": True
    }
]

print("Seeding Home FAQs...")
for item in initial_faqs:
    faq, created = HomeFAQ.objects.get_or_create(
        question=item["question"],
        defaults={
            "answer": item["answer"],
            "order": item["order"],
            "is_active": item["is_active"]
        }
    )
    if not created:
        faq.answer = item["answer"]
        faq.order = item["order"]
        faq.is_active = item["is_active"]
        faq.save()
    print(f" - {faq.question} (Order: {faq.order})")

print(f"Done! Total FAQs in database: {HomeFAQ.objects.count()}")
