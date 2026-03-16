from django.urls import path
from . import views

urlpatterns = [
    path('', views.message_list, name='q7_home'),
    path('create/', views.message_create, name='q7_create'),
]