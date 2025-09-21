# Create your models here.
# requests_app/models.py
from django.db import models
from django.conf import settings
from django.utils import timezone

class ExternalRequest(models.Model):
    STATUS_CHOICES = [
        ('submitted', 'Submitted'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed')
    ]
    code = models.CharField(max_length=64, unique=True)
    requester = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='external_requests')
    description = models.TextField()
    method = models.TextField(blank=True, null=True)  # metode analisa
    results = models.JSONField(default=dict, blank=True)  # hasil pengujian
    status = models.CharField(max_length=32, choices=STATUS_CHOICES, default='submitted')
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.code} - {self.status}"
        

class ProductDevRequest(models.Model):
    STATUS_CHOICES = [
        ('submitted', 'Submitted'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed')
    ]
    code = models.CharField(max_length=64, unique=True)
    requester = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='product_dev_requests')
    product_name = models.CharField(max_length=128)
    description = models.TextField()
    trial_results = models.JSONField(default=dict, blank=True)
    status = models.CharField(max_length=32, choices=STATUS_CHOICES, default='submitted')
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.product_name} ({self.code}) - {self.status}"
    
class ExternalAnalysisResult(models.Model):
    request = models.ForeignKey(ExternalRequest, on_delete=models.CASCADE)
    sample_code = models.CharField(max_length=64)
    parameter = models.CharField(max_length=128)
    result = models.CharField(max_length=128)
    method = models.CharField(max_length=128)
    performed_by = models.CharField(max_length=128)
    completed_at = models.DateTimeField(null=True, blank=True)

