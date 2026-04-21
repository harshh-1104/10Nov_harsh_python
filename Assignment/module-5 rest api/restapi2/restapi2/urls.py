"""
URL configuration for restapi2 project.
──────────────────────────────────────────────
Routes all traffic to the doctor_finder app.
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # Django admin panel
    path('admin/', admin.site.urls),

    # DRF browsable API login/logout (optional, handy for testing)
    path('api-auth/', include('rest_framework.urls')),

    # All doctor_finder app URLs (UI + API)
    path('', include('doctor_finder.urls')),

    # Allauth URLs
    path('accounts/', include('allauth.urls')),
]
