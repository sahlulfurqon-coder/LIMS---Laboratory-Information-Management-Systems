from django.db import models
from django.conf import settings
from django.utils import timezone

class Specification(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('pending_approval', 'Pending Approval'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('inactive', 'Inactive')
    ]

    product_name = models.CharField(max_length=128)
    version = models.PositiveIntegerField(default=1)
    parameters = models.JSONField(default=dict, blank=True)  # contoh: {"moisture": "≤5%", "fat": "≥20%"}
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='created_specs')
    created_at = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=32, choices=STATUS_CHOICES, default='draft')
    notes = models.TextField(blank=True)
    approved_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='approved_specs')
    approved_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.product_name} v{self.version} ({self.status})"

    class Meta:
        ordering = ['-created_at']
