from django.urls import path
from . import views

urlpatterns = [
    path('', views.doctor_list, name='doctor_list_ajax'),
    path('save/', views.save_doctor, name='save_doctor'),
    path('delete/', views.delete_doctor, name='delete_doctor'),
]
