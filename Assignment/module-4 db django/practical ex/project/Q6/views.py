from django.shortcuts import render, redirect
from .models import Doctor
from .forms import DoctorForm

# View to list all doctors
def doctor_list(request):
    doctors = Doctor.objects.all()
    return render(request, 'Q6/doctor_list.html', {'doctors': doctors})

# View to add a new doctor
def add_doctor(request):
    if request.method == 'POST':
        form = DoctorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('doctor_list')
    else:
        form = DoctorForm()
    return render(request, 'Q6/doctor_form.html', {'form': form})
