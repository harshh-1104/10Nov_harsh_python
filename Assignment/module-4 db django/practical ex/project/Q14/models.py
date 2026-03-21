from django.db import models

# Create your models here.

class Doctor(models.Model):
    name = models.CharField(max_length=100)
    specialization = models.CharField(max_length=100)
    hospital = models.CharField(max_length=100)
    contact = models.CharField(max_length=15)

    def __str__(self):
        return self.name
