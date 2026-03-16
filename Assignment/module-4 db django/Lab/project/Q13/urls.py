from django.urls import path
from . import views

urlpatterns = [
    path('', views.user_login, name='q13_home'),
    path('register/', views.register, name='q13_register'),
    path('login/', views.user_login, name='q13_login'),
    path('logout/', views.user_logout, name='q13_logout'),
    path('profile/', views.profile, name='q13_profile'),
]