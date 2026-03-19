from django.db import models

# Create your models here.
class Doctor(models.Model):
    name = models.CharField(max_length=100)
    specialization = models.CharField(max_length=100)
    contact_number = models.CharField(max_length=15)
    email = models.EmailField(unique=True)
    address = models.TextField()

    def __str__(self):
        return self.name
