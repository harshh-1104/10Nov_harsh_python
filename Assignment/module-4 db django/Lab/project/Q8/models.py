from django.db import models

class Doctor(models.Model):
    SPECIALTY_CHOICES = [
        ('cardiology', 'Cardiology'),
        ('dermatology', 'Dermatology'),
        ('neurology', 'Neurology'),
        ('orthopedics', 'Orthopedics'),
        ('pediatrics', 'Pediatrics'),
        ('psychiatry', 'Psychiatry'),
        ('radiology', 'Radiology'),
        ('surgery', 'Surgery'),
    ]

    name = models.CharField(max_length=100, help_text="Full name of the doctor")
    specialty = models.CharField(max_length=50, choices=SPECIALTY_CHOICES, help_text="Medical specialty")
    email = models.EmailField(unique=True, help_text="Contact email")
    phone = models.CharField(max_length=15, help_text="Phone number")
    address = models.TextField(blank=True, help_text="Clinic address")
    years_experience = models.PositiveIntegerField(default=0, help_text="Years of experience")
    is_available = models.BooleanField(default=True, help_text="Currently accepting patients")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']
        verbose_name = "Doctor"
        verbose_name_plural = "Doctors"

    def __str__(self):
        return f"Dr. {self.name} - {self.get_specialty_display()}"

