"""
Admin configuration for the Doctor Finder app.
"""
from django.contrib import admin
from .models import Doctor, OTPVerification


@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    """Admin panel configuration for Doctor model."""
    list_display = ['name', 'specialty', 'contact_details', 'created_at']
    list_filter = ['specialty', 'created_at']
    search_fields = ['name', 'specialty', 'contact_details']
    ordering = ['-created_at']


@admin.register(OTPVerification)
class OTPVerificationAdmin(admin.ModelAdmin):
    """Admin panel configuration for OTP records."""
    list_display = ['email', 'otp_code', 'is_verified', 'created_at']
    list_filter = ['is_verified']
    search_fields = ['email']
