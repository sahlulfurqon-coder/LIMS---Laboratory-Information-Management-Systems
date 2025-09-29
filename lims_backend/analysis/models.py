from django.db import models
from django.conf import settings
from django.utils import timezone
from samples.models import Sample

class AnalysisParameter(models.Model):
    name = models.CharField(max_length=100)  # e.g. Peroxide Value, Iodine Value
    unit = models.CharField(max_length=50, blank=True, null=True)  # e.g. meq/kg
    method = models.CharField(max_length=100, blank=True, null=True)  # e.g. AOCS Cd 8b-90

    def __str__(self):
        return self.name

class AnalysisResult(models.Model):
    sample = models.ForeignKey(Sample, on_delete=models.CASCADE, related_name="analyses")
    parameter = models.ForeignKey(AnalysisParameter, on_delete=models.CASCADE)
    value = models.CharField(max_length=100)  # fleksibel string, bisa angka atau teks
    status = models.CharField(
        max_length=10,
        choices=[("PASS", "Pass"), ("FAIL", "Fail")],
        blank=True,
        null=True,
    )
    analyst = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    note = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    class Meta:
        unique_together = ("sample", "parameter", "analyst")  # agar analis bisa isi masing2

    def __str__(self):
        return f"{self.sample.code} - {self.parameter.name}"