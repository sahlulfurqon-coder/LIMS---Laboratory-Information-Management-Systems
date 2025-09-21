# Create your models here.
# documents/models.py
from django.db import models
from django.conf import settings
from django.utils import timezone

class Document(models.Model):
    DOC_TYPES = [
        ('SOP', 'SOP'),
        ('WI', 'Work Instruction'),
        ('FORM', 'Form'),
        ('COA_TEMPLATE', 'COA Template')
    ]

    title = models.CharField(max_length=128)
    file = models.FileField(upload_to='documents/%Y/%m/%d/')
    doc_type = models.CharField(max_length=32, choices=DOC_TYPES)
    version = models.IntegerField(default=1)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='created_documents')
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=32, default='active')  # active / archived
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"{self.title} v{self.version}"

