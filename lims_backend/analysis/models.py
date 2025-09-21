from django.db import models
from django.conf import settings
from django.utils import timezone
from samples.models import Sample

class AnalysisParameter(models.Model):
    name = models.CharField(max_length=128)
    description = models.TextField(blank=True, null=True)
    sample_type = models.ForeignKey('samples.SampleType', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} ({self.sample_type.name})"


class AnalysisResult(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('validated', 'Validated'),
        ('rejected', 'Rejected'),
        ('released', 'Released')
    ]

    sample = models.ForeignKey(Sample, on_delete=models.CASCADE, related_name='analysis_results')
    parameter = models.ForeignKey(AnalysisParameter, on_delete=models.CASCADE)
    analyst = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    value = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=32, choices=STATUS_CHOICES, default='pending')
    notes = models.TextField(blank=True)
    registered_at = models.DateTimeField(default=timezone.now)
    validated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='validated_results', blank=True)
    validated_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ('sample', 'parameter')

    def __str__(self):
        return f"{self.sample.code} - {self.parameter.name} ({self.status})"
