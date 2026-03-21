from django.urls import path
from . import views

urlpatterns = [
    path('', views.payment_form, name='payment_form'),
    path('initiate/', views.initiate_payment, name='initiate_payment'),
    path('callback/', views.payment_callback, name='payment_callback'),
]