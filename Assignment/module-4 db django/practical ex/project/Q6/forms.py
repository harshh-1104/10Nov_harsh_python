from django import forms
from .models import Doctor

class DoctorForm(forms.ModelForm):
    class Meta:
        model = Doctor
        fields = ['name', 'specialization', 'contact_number', 'email', 'address']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Doctor Name'}),
            'specialization': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Specialization'}),
            'contact_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Contact Number'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter Email'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter Address', 'rows': 3}),
        }
