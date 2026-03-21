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

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('Q1.urls')),
    path('', include('Q2.urls')),
    path('', include('Q3.urls')),
    path('q6/', include('Q6.urls')),
    path('q7/', include('Q7.urls')),
    path('q9/', include('Q9.urls')),
    path('q10/', include('Q10.urls')),
    path('q11/', include('Q11.urls')),
    path('q12/', include('Q12.urls')),
    path('q13/', include('Q13.urls')),
    path('q14/', include('Q14.urls')),
]
