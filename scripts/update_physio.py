import os
import sys
import django

# Setup Django
sys.path.append(os.getcwd())
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from api.models import Service

def update():
    try:
        s = Service.objects.get(slug='physiotherapy')
        s.description = """<p class="lead text-lg mb-6">Physiotherapy plays an important role in managing a wide range of conditions. Early treatment often leads to faster recovery and helps prevent long-term complications.</p>

<h3 class="text-xl font-semibold mt-10 mb-4 text-[#001D3D]">Conditions Managed with Physiotherapy Services</h3>
<p class="mb-4">Common problems treated include:</p>
<ul class="list-disc pl-6 mb-8 space-y-2 text-gray-600">
  <li>Back and neck pain</li>
  <li>Knee pain and joint stiffness</li>
  <li>Shoulder pain and limited movement</li>
  <li>Sports injuries and muscle strains</li>
  <li>Robotic Surgery rehabilitation</li>
  <li>Arthritis and age-related joint issues</li>
  <li>Deformity Corrections</li>
  <li>Hip Joint Replacement rehabilitation</li>
</ul>

<h3 class="text-xl font-semibold mt-10 mb-4 text-[#001D3D]">Benefits of Physiotherapy Treatment</h3>
<p class="mb-4">Focused on restoring movement, reducing pain, and helping you return to your daily activities with confidence. Patients commonly experience:</p>
<ul class="list-disc pl-6 mb-8 space-y-2 text-gray-600">
  <li>Reduction in pain and inflammation</li>
  <li>Improved movement and flexibility</li>
  <li>Faster recovery after injury or surgery</li>
  <li>Better strength and stability</li>
  <li>Reduced dependence on medications</li>
</ul>
<p class="italic text-gray-500 mt-4">With the right treatment plan, most patients notice gradual but steady improvement.</p>

<h3 class="text-xl font-semibold mt-10 mb-4 text-[#001D3D]">Expert Home Treatment with Dr. Ulhas Sonar</h3>
<p class="mb-6 text-gray-600">Dr. Ulhas provides physiotherapy services for individuals of all ages from pediatric to geriatric care, with proper care and concerns.</p>"""
        
        s.items = [
            "DHA Licensed Experts",
            "Flexible Home Visits",
            "Personalized Care Plans",
            "No Hidden Charges"
        ]
        
        s.faqs = [
            {
                "question": "How much does physiotherapy cost in Dubai?",
                "answer": "The cost depends on the type of treatment and number of sessions required. Flexible packages are available to make treatment more affordable."
            },
            {
                "question": "Is physiotherapy at home effective?",
                "answer": "Yes, home physiotherapy is equally effective when delivered by qualified professionals. It also improves convenience and consistency."
            },
            {
                "question": "How many physiotherapy sessions will I need?",
                "answer": "This depends on your condition. Some patients improve within a few sessions, while others may require a structured rehabilitation program."
            }
        ]
        s.save()
        print("Updated physiotherapy service successfully in the database!")
    except Service.DoesNotExist:
        print("Service with slug 'physiotherapy' does not exist in the database.")

if __name__ == '__main__':
    update()
