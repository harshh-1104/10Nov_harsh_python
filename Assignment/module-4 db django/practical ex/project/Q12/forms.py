from django import forms
from .models import Doctor

class DoctorForm(forms.ModelForm):
    class Meta:
        model = Doctor
        fields = ['name', 'specialization', 'contact_number', 'email']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter doctor name'}),
            'specialization': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter specialization'}),
            'contact_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter contact number'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter email address'}),
        }
