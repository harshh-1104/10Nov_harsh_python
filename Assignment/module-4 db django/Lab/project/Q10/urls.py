from django.urls import path
from . import views

urlpatterns = [
    path('', views.register, name='q10_register'),
]