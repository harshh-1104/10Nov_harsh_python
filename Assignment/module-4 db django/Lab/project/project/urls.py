"""
URL configuration for project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from Q1 import views as q1_views
from Q2 import views as q2_views
from Q3 import views as q3_views
from Q4 import views as q4_views

urlpatterns = [
    path('', q1_views.home, name='home'),
    path('q2/', q2_views.home, name='q2_home'),
    path('q3/', q3_views.home, name='q3_home'),
    path('q4/', q4_views.home, name='q4_home'),
    path('q6/', include('Q6.urls')),
    path('q7/', include('Q7.urls')),
    path('admin/', admin.site.urls),
]
