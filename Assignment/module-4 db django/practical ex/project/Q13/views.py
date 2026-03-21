from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from .forms import SignUpForm, ProfileUpdateForm

# Create your views here.

class SignUpView(CreateView):
    form_class = SignUpForm
    success_url = reverse_lazy('login')
    template_name = 'Q13/signup.html'

class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'Q13/dashboard.html'

class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = ProfileUpdateForm
    template_name = 'Q13/profile.html'
    success_url = reverse_lazy('dashboard')

    def get_object(self):
        return self.request.user
