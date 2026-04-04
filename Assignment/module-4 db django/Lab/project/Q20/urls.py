from django.urls import path
from . import views

urlpatterns = [
    path('', views.doctor_map_view, name='doctor_map'),
]
