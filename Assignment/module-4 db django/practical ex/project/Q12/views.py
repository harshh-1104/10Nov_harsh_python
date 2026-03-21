from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .models import Doctor
from .forms import DoctorForm

# Create your views here.

class DoctorListView(ListView):
    model = Doctor
    template_name = 'Q12/doctor_list.html'
    context_object_name = 'doctors'

class DoctorCreateView(CreateView):
    model = Doctor
    form_class = DoctorForm
    template_name = 'Q12/doctor_form.html'
    success_url = reverse_lazy('doctor_list')

class DoctorUpdateView(UpdateView):
    model = Doctor
    form_class = DoctorForm
    template_name = 'Q12/doctor_form.html'
    success_url = reverse_lazy('doctor_list')

class DoctorDeleteView(DeleteView):
    model = Doctor
    template_name = 'Q12/doctor_confirm_delete.html'
    success_url = reverse_lazy('doctor_list')
