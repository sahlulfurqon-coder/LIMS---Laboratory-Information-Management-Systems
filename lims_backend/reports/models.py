# Create your models here.
# reports/models.py
from django.db import models
from django.conf import settings
from django.utils import timezone

class AuditTrail(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    action = models.CharField(max_length=256)  # misal: "Update Sample", "Approve Spec"
    object_type = models.CharField(max_length=64)  # model name
    object_id = models.IntegerField(null=True, blank=True)
    timestamp = models.DateTimeField(default=timezone.now)
    details = models.JSONField(default=dict, blank=True)  # simpan snapshot perubahan

    def __str__(self):
        return f"{self.timestamp} - {self.user} - {self.action}"
