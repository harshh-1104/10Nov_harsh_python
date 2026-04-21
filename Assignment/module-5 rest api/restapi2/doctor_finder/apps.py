from django.apps import AppConfig


class DoctorFinderConfig(AppConfig):
    """Configuration for the doctor_finder app."""
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'doctor_finder'
    verbose_name = 'Doctor Finder API'
