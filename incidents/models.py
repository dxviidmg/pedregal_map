from django.db import models


class Incident(models.Model):
    CATEGORY_CHOICES = [
        ('A', 'Accidentes'),
        ('U', 'Urbanidad'),
        ('V', 'Vialidad'),
    ]

    SEVERITY_CHOICES = [
        ('B', 'Baja'),
        ('M', 'Media'),
        ('A', 'Alta'),
    ]

    STATUS_CHOICES = [
        ('A', 'Abierto'),
        ('E', 'En proceso'),
        ('C', 'Cerrado'),
    ]

    category = models.CharField(max_length=1, choices=CATEGORY_CHOICES)
    severity = models.CharField(max_length=1, choices=SEVERITY_CHOICES)
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='A')
    title = models.CharField(max_length=50)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    latitude = models.DecimalField(max_digits=10, decimal_places=7)
    longitude = models.DecimalField(max_digits=10, decimal_places=7)

    def __str__(self):
        return self.title