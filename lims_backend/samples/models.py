# samples/models.py
from django.db import models
from django.conf import settings
from django.utils import timezone

class SampleType(models.Model):
    name = models.CharField(max_length=128)   # Raw Material / Fat Blend / Finished Product
    category = models.CharField(max_length=64, blank=True)  # Oil / Packaging / dll
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.name} ({self.category})" if self.category else self.name


class RawMaterial(models.Model):
    type = models.ForeignKey(SampleType, on_delete=models.CASCADE, related_name="raw_details")
    name = models.CharField(max_length=128)  # Olein, Stearin, SPMF, RBD PO, RCNO, dll
    variant = models.CharField(max_length=128, blank=True)  # e.g. Low GE / Normal / Hard / Soft
    editable = models.BooleanField(default=True)  # bisa ditambah oleh Admin/QA/RnD
    def __str__(self):
        return f"{self.name} {self.variant}".strip()


class Sample(models.Model):
    SAMPLE_STATUS = [
        ("registered","Registered"),
        ("assigned","Assigned"),
        ("in_analysis","In Analysis"),
        ("completed","Completed"),
        ("deleted","Deleted")
    ]
    code = models.CharField(max_length=64, unique=True)
    type = models.ForeignKey(SampleType, on_delete=models.SET_NULL, null=True)
    detail = models.ForeignKey(RawMaterialDetail, on_delete=models.SET_NULL, null=True, blank=True)
    requester = models.CharField(max_length=128, blank=True)
    registered_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name="registered_samples")
    registered_at = models.DateTimeField(default=timezone.now)
    received_at = models.DateTimeField(null=True, blank=True)
    urgency = models.CharField(max_length=32, default="normal")  # normal/urgent
    status = models.CharField(max_length=32, choices=SAMPLE_STATUS, default="registered")
    notes = models.TextField(blank=True)
    raw_meta = models.JSONField(default=dict, blank=True)  # tank info, batch info, transfer info

    def __str__(self):
        return f"{self.code} - {self.type}"


class FatBlend(models.Model):
    fatblend = models.ForeignKey(Sample, on_delete=models.CASCADE, related_name="blend_components")
    raw_material = models.ForeignKey(RawMaterialDetail, on_delete=models.CASCADE)
    percentage = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return f"{self.fatblend.code}: {self.raw_material} ({self.percentage}%)"
