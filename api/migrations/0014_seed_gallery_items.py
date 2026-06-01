from django.db import migrations

def seed_gallery_items(apps, schema_editor):
    GalleryItem = apps.get_model('api', 'GalleryItem')
    
    gallery_items = [
        {
            "title": "Patient Testimonials",
            "description": "Exceptional patient satisfaction and positive feedback from those who have undergone treatment with Dr. Ulhas.",
            "category": "About",
            "span": "col-span-2 row-span-2",
            "image": "gallery/gallery_1.webp",
            "order": 1
        },
        {
            "title": "Excellence Recognition",
            "description": "Dr. Ulhas Sonar receiving recognition for outstanding clinical contributions and surgical excellence.",
            "category": "Awards",
            "span": "col-span-1 row-span-1",
            "image": "gallery/gallery_2.webp",
            "order": 2
        },
        {
            "title": "Clinical Excellence Award",
            "description": "Honouring the dedication to patient care and surgical innovation in the field of orthopedics.",
            "category": "Awards",
            "span": "col-span-1 row-span-1",
            "image": "gallery/gallery_3.webp",
            "order": 3
        },
        {
            "title": "Our Dedicated Team",
            "description": "A cohesive team of healthcare professionals committed to delivering world-class orthopedic care.",
            "category": "Clinic",
            "span": "col-span-1 row-span-2",
            "image": "gallery/gallery_4.webp",
            "order": 4
        },
        {
            "title": "Advanced Surgical Precision",
            "description": "Intra-operative perspective showcasing the meticulous approach to joint preservation and replacement.",
            "category": "Surgery",
            "span": "col-span-1 row-span-1",
            "image": "gallery/gallery_5.webp",
            "order": 5
        },
        {
            "title": "Team Collaboration",
            "description": "Regular clinical meetings and team celebrations to ensure excellence in patient care pathways.",
            "category": "Clinic",
            "span": "col-span-1 row-span-1",
            "image": "gallery/gallery_6.webp",
            "order": 6
        },
        {
            "title": "Team Social Engagement",
            "description": "Fostering strong professional relationships through social events and team-building activities.",
            "category": "Clinic",
            "span": "col-span-1 row-span-1",
            "image": "gallery/gallery_7.webp",
            "order": 7
        },
        {
            "title": "Professional Growth",
            "description": "Celebrating milestones and collective achievements in our journey of clinical excellence.",
            "category": "Clinic",
            "span": "col-span-1 row-span-1",
            "image": "gallery/gallery_8.webp",
            "order": 8
        },
        {
            "title": "Global Orthopedic Networking",
            "description": "Exchanging knowledge and surgical concepts with international colleagues at global conferences.",
            "category": "Conference",
            "span": "col-span-1 row-span-1",
            "image": "gallery/gallery_9.webp",
            "order": 9
        },
        {
            "title": "Comprehensive Knee Assessment",
            "description": "Detailed examination focusing on biomechanics and joint health for personalized recovery.",
            "category": "Clinic",
            "span": "col-span-1 row-span-1",
            "image": "gallery/kneeassessment.webp",
            "order": 10
        },
        {
            "title": "Shoulder Mobility Care",
            "description": "Expert assessment and management of rotator cuff injuries and shoulder instability.",
            "category": "Clinic",
            "span": "col-span-1 row-span-1",
            "image": "gallery/shoulderassessment.webp",
            "order": 11
        },
        {
            "title": "Hip Preservation Strategies",
            "description": "Specialized interventions designed to preserve the joint and delay degenerative changes.",
            "category": "Clinic",
            "span": "col-span-1 row-span-1",
            "image": "gallery/hipassessment.webp",
            "order": 12
        },
        {
            "title": "Spine & Back Health",
            "description": "Multidisciplinary approach to managing chronic back pain and spinal conditions.",
            "category": "Clinic",
            "span": "col-span-1 row-span-1",
            "image": "gallery/spineassessment.webp",
            "order": 13
        },
        {
            "title": "Elite Sports Recovery",
            "description": "Advanced surgical and biological treatments to return athletes to their peak performance.",
            "category": "Surgery",
            "span": "col-span-1 row-span-1",
            "image": "gallery/sportsrecovery.webp",
            "order": 14
        },
        {
            "title": "Hand & Wrist Precision",
            "description": "Delicate care for carpal tunnel, tendon injuries, and arthritic hand conditions.",
            "category": "Clinic",
            "span": "col-span-1 row-span-1",
            "image": "gallery/handwristcare.webp",
            "order": 15
        },
        {
            "title": "Combined Limb Procedures",
            "description": "Holistic surgical management of complex lower limb injuries and deformities.",
            "category": "Surgery",
            "span": "col-span-1 row-span-1",
            "image": "gallery/combinedjoint.webp",
            "order": 16
        }
    ]
    
    # Delete existing to prevent duplication
    GalleryItem.objects.all().delete()
    
    for item in gallery_items:
        GalleryItem.objects.create(
            title=item["title"],
            description=item["description"],
            category=item["category"],
            span=item["span"],
            image=item["image"],
            order=item["order"]
        )

def rollback_seed(apps, schema_editor):
    GalleryItem = apps.get_model('api', 'GalleryItem')
    GalleryItem.objects.all().delete()

class Migration(migrations.Migration):

    dependencies = [
        ('api', '0013_galleryitem'),
    ]

    operations = [
        migrations.RunPython(seed_gallery_items, rollback_seed),
    ]
