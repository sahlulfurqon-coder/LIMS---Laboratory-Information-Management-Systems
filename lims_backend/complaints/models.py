# complaints/models.py
from django.db import models
from django.conf import settings
from django.utils import timezone

class Complaint(models.Model):
    STATUS_CHOICES = [
        ('open', 'Open'),
        ('in_progress', 'In Progress'),
        ('closed', 'Closed')
    ]

    code = models.CharField(max_length=64, unique=True)
    title = models.CharField(max_length=128)
    description = models.TextField()
    submitted_by = models.CharField(max_length=128, blank=True)  # bisa customer/internal
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='created_complaints')
    created_at = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=32, choices=STATUS_CHOICES, default='open')
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"{self.code} - {self.title}"


class CAPA(models.Model):
    complaint = models.ForeignKey("Complaint", on_delete=models.CASCADE, related_name="capas")
    action = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True) 
    updated_at = models.DateTimeField(auto_now=True)
