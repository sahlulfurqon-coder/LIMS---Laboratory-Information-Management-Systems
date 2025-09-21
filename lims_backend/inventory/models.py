# Create your models here.
# inventory/models.py
from django.db import models
from django.conf import settings
from django.utils import timezone

class InventoryItem(models.Model):
    ITEM_TYPE = [('chemical','Chemical'),('standard','Standard'),('consumable','Consumable')]
    name = models.CharField(max_length=128)
    type = models.CharField(max_length=32, choices=ITEM_TYPE)
    quantity = models.FloatField(default=0)
    unit = models.CharField(max_length=32, default='pcs')
    min_stock = models.FloatField(default=0)  # untuk alert <20%
    expired_date = models.DateField(null=True, blank=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.name} ({self.type})"

class InventoryUsage(models.Model):
    item = models.ForeignKey(InventoryItem, on_delete=models.CASCADE, related_name='usages')
    used_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    quantity = models.FloatField()
    usage_date = models.DateTimeField(default=timezone.now)
    notes = models.TextField(blank=True)

class InventoryOrder(models.Model):
    item = models.ForeignKey(InventoryItem, on_delete=models.CASCADE, related_name='orders')
    requested_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    quantity = models.FloatField()
    status = models.CharField(max_length=32, choices=[('pending','Pending'),('ordered','Ordered'),('received','Received')], default='pending')
    requested_at = models.DateTimeField(default=timezone.now)
