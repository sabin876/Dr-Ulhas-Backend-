import sys
import os
import django

# Set up Django environment
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from api.models import Service, SubService

def populate():
    try:
        service = Service.objects.get(slug='fracture-trauma-surgery')
        print(f"Found service: {service.title} (ID: {service.id})")
        
        # Clear existing subservices
        print("Clearing existing sub-services...")
        SubService.objects.filter(service=service).delete()
        
        # List of actual sub-services
        fracture_subservices = [
            {
                "title": "Fracture Assessment",
                "desc": "Fracture assessment includes specialist evaluation of bone injuries, swelling, pain, deformity and difficulty using the affected limb. The consultation may include clinical examination, review of X-rays, CT scans or MRI scans, and discussion of the most suitable treatment pathway."
            },
            {
                "title": "Fracture Fixation Surgery",
                "desc": "Fracture fixation surgery is used for selected fractures that are displaced, unstable, involve a joint, or are unlikely to heal well with non-surgical care alone. Fixation may involve plates, screws, nails or wires depending on the fracture pattern, bone involved, soft-tissue condition and patient needs."
            },
            {
                "title": "Upper Limb Fracture Treatment",
                "desc": "Upper limb fracture treatment includes care for fractures of the shoulder, arm, elbow, forearm, wrist and hand. These injuries may affect lifting, gripping, writing, driving, work and daily function, so treatment is planned with attention to bone healing, joint movement and hand or arm use."
            },
            {
                "title": "Lower Limb Fracture Treatment",
                "desc": "Lower limb fracture treatment includes care for fractures of the hip, thigh, knee, leg, ankle and foot. Because these injuries can affect walking and weight-bearing, treatment focuses on fracture stability, safe mobilisation, pain control and gradual return to activity."
            },
            {
                "title": "Wrist Fracture Surgery",
                "desc": "Wrist fracture surgery may be needed for selected distal radius fractures and other wrist fractures when alignment is poor, the fracture is unstable or joint involvement is present. Some wrist fractures can be treated with plaster or splinting, while others may require fixation to support better alignment and hand function."
            },
            {
                "title": "Ankle Fracture Treatment",
                "desc": "Ankle fracture treatment includes assessment of stable and unstable ankle injuries. Stable fractures may be managed with immobilisation and rehabilitation, while displaced or unstable fractures may require surgical fixation to restore ankle alignment and support safe walking."
            },
            {
                "title": "Hip Fracture Surgery",
                "desc": "Hip fracture surgery may be required for selected hip fractures, especially when walking ability, fracture type and patient health indicate the need for fixation or replacement. Treatment depends on the fracture pattern, bone quality, age, general health and mobility needs."
            },
            {
                "title": "Ligament and Soft-Tissue Injury Care",
                "desc": "Ligament and soft-tissue injury care includes treatment for sprains, ligament injuries, muscle injuries and tendon-related problems. Treatment may involve rest, bracing, physiotherapy, activity modification, imaging review or surgery when instability or significant structural damage is present."
            },
            {
                "title": "Minor Injury and Sports Trauma Care",
                "desc": "Minor injury and sports trauma care includes assessment and treatment of common injuries such as falls, twists, sprains, bruising and activity-related trauma. Early assessment is useful when pain, swelling, difficulty walking or reduced movement continues after the injury."
            },
            {
                "title": "General Orthopaedic Consultation",
                "desc": "A general orthopaedic consultation is suitable for bone, joint, muscle, tendon and ligament problems affecting daily activities, work, walking or sport. This may include assessment of persistent pain, stiffness, swelling, weakness, movement restriction or reduced confidence after injury."
            },
            {
                "title": "Post-Fracture Rehabilitation Planning",
                "desc": "Post-fracture rehabilitation planning supports recovery after plaster treatment, splinting, bracing or fracture surgery. The plan may include mobilisation, range-of-motion exercises, strengthening, walking support, balance training and gradual return to daily activity."
            },
            {
                "title": "Second Opinion for Fracture Treatment",
                "desc": "A second opinion for fracture treatment may help patients who want clarity about X-rays, scans, plaster treatment, surgery, healing progress or delayed recovery. This consultation helps explain the diagnosis, treatment options, expected recovery, and whether current management is suitable."
            }
        ]
        
        print("Inserting 12 new sub-services...")
        for item in fracture_subservices:
            ss = SubService.objects.create(
                service=service,
                title=item["title"],
                description=item["desc"]
            )
            print(f"Created Sub-Service: {ss.title} (Slug: {ss.slug})")
            
        print("Successfully populated all sub-services!")
        
    except Service.DoesNotExist:
        print("Error: 'fracture-trauma-surgery' service not found in database!")
    except Exception as e:
        print(f"Error occurred: {e}")

if __name__ == '__main__':
    populate()
