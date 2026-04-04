from django.shortcuts import render
from .models import Doctor
import json

def doctor_map_view(request):
    doctors = Doctor.objects.all()
    # Prepare doctors data for JavaScript
    doctors_list = []
    for doc in doctors:
        doctors_list.append({
            'name': doc.name,
            'specialty': doc.specialty,
            'address': doc.address,
            'lat': float(doc.latitude),
            'lng': float(doc.longitude),
            'phone': doc.phone
        })
    
    context = {
        'doctors_json': json.dumps(doctors_list)
    }
    return render(request, 'Q20/map.html', context)
