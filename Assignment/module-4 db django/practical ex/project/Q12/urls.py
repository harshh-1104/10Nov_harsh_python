from django.urls import path
from . import views

urlpatterns = [
    path('', views.DoctorListView.as_view(), name='doctor_list'),
    path('add/', views.DoctorCreateView.as_view(), name='doctor_add'),
    path('edit/<int:pk>/', views.DoctorUpdateView.as_view(), name='doctor_edit'),
    path('delete/<int:pk>/', views.DoctorDeleteView.as_view(), name='doctor_delete'),
]
