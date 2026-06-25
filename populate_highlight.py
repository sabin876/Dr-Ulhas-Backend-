import os
import sys
import django
import json

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from api.models import Service

s = Service.objects.first()

s.highlight_badge = "Expertise & Precision"
s.highlight_title = "Why Choose Dr Ulhas Sonar for Robotic Knee Replacement Surgery in Pune?"
s.highlight_description = "<p>Patients seeking robotic knee surgery in Pune often look for more than technology alone. True success comes from a combination of advanced tools and an expert surgeon's touch.</p>"
s.highlight_checklist_title = "Successful knee replacement requires:"
s.highlight_checklist_items = [
    "Accurate diagnosis",
    "Appropriate patient selection",
    "Detailed surgical planning",
    "Technical precision",
    "Structured rehabilitation"
]
s.highlight_doctor_name = "Dr Ulhas Sonar"
s.highlight_doctor_role = "Consultant Orthopedic Surgeon"
s.highlight_doctor_badges = ["UK-TRAINED", "FRCS (ENG)"]
s.highlight_doctor_description = "<p>Dr Ulhas Sonar is a UK-trained Orthopedic Surgeon with FRCS (England) and European Board Certification in Orthopedics. His practice focuses on knee reconstruction, robotic knee replacement, sports injuries, and knee preservation procedures.</p>"

s.save()
print("Populated database with the Highlight Section content successfully!")
