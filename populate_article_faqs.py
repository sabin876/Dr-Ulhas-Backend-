import os
import sys
import json
import django

sys.path.append(os.getcwd())
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from api.models import Article

article_faqs_map = {
    'causes-of-knee-pain': [
        {
            "question": "What is the most common cause of knee pain after physical activity?",
            "answer": "Common causes after physical activity include ligament sprains, meniscus tears, patellar tendonitis, or joint overload. Proper diagnosis by a specialist determines the exact cause."
        },
        {
            "question": "Is knee pain always caused by arthritis?",
            "answer": "No. While osteoarthritis is common in older adults, knee pain in younger and active individuals is frequently caused by sports injuries, patellofemoral pain syndrome, or muscle imbalances."
        },
        {
            "question": "When should I see a doctor for knee pain?",
            "answer": "You should consult a doctor if your knee pain causes persistent swelling, instability ('giving way'), inability to bear weight, or stiffness that does not improve after 48 hours."
        }
    ],
    'knee-pain-gym-sports': [
        {
            "question": "How can I tell the difference between muscle soreness and joint injury after gym?",
            "answer": "Muscle soreness typically peaks within 24–48 hours, feels like a dull ache across muscle bellies, and resolves. Joint or ligament injuries produce sharp localized pain, swelling, locking, or instability."
        },
        {
            "question": "Should I stop exercising completely if my knee hurts?",
            "answer": "You should temporarily pause heavy leg workouts, deep squats, and high-impact sports. Switch to low-impact activities like swimming or light stationary cycling while getting evaluated."
        }
    ],
    'when-to-get-mri-knee': [
        {
            "question": "Is an X-ray enough to diagnose knee pain?",
            "answer": "X-rays are excellent for evaluating bones and joint alignment, but an MRI is essential for visualizing soft tissue structures like the ACL, MCL, meniscus, and articular cartilage."
        },
        {
            "question": "Do I need an urgent MRI after a knee injury?",
            "answer": "An urgent MRI is recommended if you heard a 'pop' during injury, experienced immediate joint swelling, or are unable to straighten or stand on your leg."
        }
    ],
    'continuing-sports-risks': [
        {
            "question": "What are the risks of playing sports with an untreated knee injury?",
            "answer": "Playing sports on an injured knee can turn partial ligament or meniscus tears into complete ruptures, cause secondary cartilage damage, and lead to premature joint degeneration."
        }
    ],
    'anterior-knee-pain-office': [
        {
            "question": "Why does prolonged sitting cause front knee pain (Movie-Goer's Sign)?",
            "answer": "Prolonged knee flexion at 90 degrees increases pressure between the kneecap (patella) and thigh bone, tightening surrounding tendons and provoking patellofemoral discomfort."
        }
    ],
    'meniscus-tear-vs-strain': [
        {
            "question": "Can a meniscus tear heal without surgery?",
            "answer": "Tears in the outer 'red zone' of the meniscus have blood supply and can heal with conservative physical therapy. Inner 'white zone' tears may require micro-invasive arthroscopy if symptomatic."
        }
    ],
    'knee-pain-exercises-desk': [
        {
            "question": "What quick exercises relieve knee stiffness at work?",
            "answer": "Seated leg extensions, ankle pumps, and gentle hamstring stretches done for 5 minutes every 2 hours help circulate synovial fluid and relieve knee tightness."
        }
    ],
    'knee-pain-travel-flights': [
        {
            "question": "How can I prevent knee pain during long flights?",
            "answer": "Wear comfortable shoes, perform isometric quad squeezes and ankle circles in your seat, walk up and down the aisle every 1-2 hours, and stay well hydrated."
        }
    ],
    'knee-pain-pillar': [
        {
            "question": "When is joint preservation preferred over knee replacement?",
            "answer": "Joint preservation techniques (such as osteotomy or cartilage restoration) are preferred in active or younger patients to preserve natural knee structures and delay or prevent joint replacement."
        }
    ]
}

print("Updating article FAQs in database...")
updated_count = 0

for article in Article.objects.all():
    faqs_list = article_faqs_map.get(article.slug, [
        {
            "question": "When should I consult an orthopedic specialist for knee pain?",
            "answer": "You should consult a specialist if your knee pain persists for more than a few days, causes swelling, prevents weight-bearing, or is accompanied by stiffness or instability."
        },
        {
            "question": "Can knee injuries heal without surgery?",
            "answer": "Yes, many non-structural knee conditions and minor sprains heal well with targeted physical therapy, activity modification, and medical management."
        }
    ])
    article.faqs = faqs_list
    article.save()
    updated_count += 1
    print(f"Updated article '{article.slug}' with {len(faqs_list)} FAQs.")

print(f"Done! Updated {updated_count} articles.")
