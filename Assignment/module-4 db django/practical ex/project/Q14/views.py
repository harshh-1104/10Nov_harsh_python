from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .models import Doctor
from .forms import DoctorForm
from django.template.loader import render_to_string

# Create your views here.

def doctor_list(request):
    doctors = Doctor.objects.all()
    return render(request, 'Q14/index.html', {'doctors': doctors})

def save_doctor(request):
    data = dict()
    if request.method == 'POST':
        pk = request.POST.get('pk')
        if pk:
            doctor = get_object_or_404(Doctor, pk=pk)
            form = DoctorForm(request.POST, instance=doctor)
        else:
            form = DoctorForm(request.POST)
        
        if form.is_valid():
            form.save()
            data['form_is_valid'] = True
            doctors = Doctor.objects.all()
            data['html_doctor_list'] = render_to_string('Q14/doctor_rows.html', {'doctors': doctors})
        else:
            data['form_is_valid'] = False
    return JsonResponse(data)

def delete_doctor(request):
    data = dict()
    if request.method == 'POST':
        pk = request.POST.get('pk')
        doctor = get_object_or_404(Doctor, pk=pk)
        doctor.delete()
        data['success'] = True
        doctors = Doctor.objects.all()
        data['html_doctor_list'] = render_to_string('Q14/doctor_rows.html', {'doctors': doctors})
    return JsonResponse(data)
