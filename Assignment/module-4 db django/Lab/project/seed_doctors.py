import os
import django

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
django.setup()

from Q20.models import Doctor

def seed():
    # Only seed if no doctors exist
    if Doctor.objects.exists():
        print("Doctors already exist. Skipping seed.")
        return

    doctors_data = [
        {
            "name": "Amit Sharma",
            "specialty": "Cardiologist",
            "address": "Ring Road, Surat, Gujarat",
            "latitude": 21.1963,
            "longitude": 72.8273,
            "phone": "+91 98765 43210"
        },
        {
            "name": "Priya Patel",
            "specialty": "Dermatologist",
            "address": "Adajan, Surat, Gujarat",
            "latitude": 21.1925,
            "longitude": 72.7917,
            "phone": "+91 91234 56789"
        },
        {
            "name": "Rahul Mehta",
            "specialty": "Neurologist",
            "address": "Vesu, Surat, Gujarat",
            "latitude": 21.1415,
            "longitude": 72.7686,
            "phone": "+91 88888 77777"
        },
        {
            "name": "Sneha Reddy",
            "specialty": "Pediatrician",
            "address": "Varachha, Surat, Gujarat",
            "latitude": 21.2121,
            "longitude": 72.8585,
            "phone": "+91 77777 66666"
        }
    ]

    for data in doctors_data:
        Doctor.objects.create(**data)
    
    print(f"Successfully seeded {len(doctors_data)} doctors.")

if __name__ == "__main__":
    seed()
