"""
Models for the Doctor Finder app.
──────────────────────────────────────────────
Defines the Doctor model with name, specialty,
contact details, and automatic timestamps.
"""
from django.db import models


class Doctor(models.Model):
    """
    Represents a doctor in the system.

    Fields:
        name            – Full name of the doctor
        specialty       – Medical specialty (e.g. Cardiology, Pediatrics)
        contact_details – Phone number or email
        created_at      – Auto-set when record is created
        updated_at      – Auto-set on every save
    """

    # ── Specialty choices (optional — allows free text too) ──
    SPECIALTY_CHOICES = [
        ('Cardiology', 'Cardiology'),
        ('Dermatology', 'Dermatology'),
        ('Neurology', 'Neurology'),
        ('Orthopedics', 'Orthopedics'),
        ('Pediatrics', 'Pediatrics'),
        ('Psychiatry', 'Psychiatry'),
        ('General', 'General Medicine'),
        ('ENT', 'ENT'),
        ('Ophthalmology', 'Ophthalmology'),
        ('Gynecology', 'Gynecology'),
    ]

    name = models.CharField(
        max_length=200,
        help_text="Full name of the doctor"
    )
    specialty = models.CharField(
        max_length=100,
        choices=SPECIALTY_CHOICES,
        default='General',
        help_text="Medical specialty"
    )
    contact_details = models.CharField(
        max_length=200,
        help_text="Phone number or email address"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']            # Newest first
        verbose_name_plural = 'Doctors'

    def __str__(self):
        return f"Dr. {self.name} — {self.specialty}"


class OTPVerification(models.Model):
    """
    Stores OTP codes for mock email/phone verification.

    Fields:
        email      – The email the OTP was sent to
        otp_code   – 6-digit verification code
        is_verified – Whether the user verified the OTP
        created_at  – When the OTP was generated
    """
    email = models.EmailField()
    otp_code = models.CharField(max_length=6)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"OTP for {self.email} ({'✓' if self.is_verified else '✗'})"
