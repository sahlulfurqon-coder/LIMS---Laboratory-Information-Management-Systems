from django.db import models
from django.conf import settings
from django.utils import timezone

# pilihan tank (gabungan J2–J13 dan TA–TF)
TANK_CHOICES = [
    *[(f"J{i}", f"J{i}") for i in range(2, 14)],  # J2 - J13
    ("TA", "TA"),
    ("TB", "TB"),
    ("TC", "TC"),
    ("TD", "TD"),
    ("TE", "TE"),
    ("TF", "TF"),
]


class SampleType(models.Model):
    name = models.CharField(max_length=128)   # Raw Material / Fat Blend / Finished Product
    category = models.CharField(max_length=64, blank=True)  # Oil / Packaging / dll
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.name} ({self.category})" if self.category else self.name


class RawMaterial(models.Model):
    type = models.ForeignKey(
        SampleType, on_delete=models.CASCADE, related_name="raw_details"
    )
    name = models.CharField(max_length=128)  # Olein, Stearin, SPMF, RBD PO, RCNO, dll
    variant = models.CharField(max_length=128, blank=True)  # e.g. Low GE / Normal / Hard / Soft
    editable = models.BooleanField(default=True)  # bisa ditambah oleh Admin/QA/RnD

    def __str__(self):
        return f"{self.name} {self.variant}".strip()


class Sample(models.Model):
    STATUS_CHOICES = [
        ("REGISTERED", "Registered"),
        ("IN_ANALYSIS", "In Analysis"),
        ("IN_APPROVAL", "In Approval"),
        ("APPROVED", "Approved"),
        ("REJECTED", "Rejected"),
        ("DELETED", "Deleted"),
    ]

    code = models.CharField(max_length=50, unique=True)
    type = models.ForeignKey(SampleType, on_delete=models.CASCADE)
    detail = models.ForeignKey(RawMaterial, on_delete=models.CASCADE, blank=True, null=True)
    tank = models.CharField(max_length=10, choices=TANK_CHOICES, blank=True, null=True)

    registered_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="registered_samples"
    )
    registered_at = models.DateTimeField(default=timezone.now)
    received_at = models.DateTimeField(blank=True, null=True)

    urgency = models.CharField(
        max_length=20,
        choices=[("normal", "Normal"), ("urgent", "Urgent")],
        default="normal",
    )
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default="REGISTERED"
    )
    notes = models.TextField(blank=True, null=True)
    raw_meta = models.JSONField(default=dict, blank=True)  # info tambahan opsional

    approved_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="approved_samples",
    )
    approval_note = models.TextField(blank=True, null=True)
    approved_at = models.DateTimeField(blank=True, null=True)

    def subtype(self):
        """Tampilkan varian raw material jika ada."""
        return self.detail.variant if self.detail and self.detail.variant else "-"

    subtype.short_description = "Subtype"  # supaya label di admin lebih rapih

    def __str__(self):
        return f"{self.code} - {self.type}"


class FatBlend(models.Model):
    fatblend = models.ForeignKey(
        Sample, on_delete=models.CASCADE, related_name="blend_components"
    )
    raw_material = models.ForeignKey(RawMaterial, on_delete=models.CASCADE)
    percentage = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return f"{self.fatblend.code}: {self.raw_material} ({self.percentage}%)"


class Packaging(models.Model):
    name = models.CharField(max_length=128, unique=True)  # Pail, Box, Dus, Jerrycan, Plastik, dll
    description = models.TextField(blank=True, null=True)
    editable = models.BooleanField(default=True)  # Bisa ditambah Admin/QA/RnD

    def __str__(self):
        return self.name


class FinishedProduct(models.Model):
    name = models.CharField(max_length=128)
    batch_code = models.CharField(max_length=64, unique=True)
    fatblend = models.ForeignKey("FatBlend", on_delete=models.SET_NULL, null=True, blank=True)
    packaging = models.ForeignKey("Packaging", on_delete=models.SET_NULL, null=True, blank=True)
    additives = models.JSONField(default=dict, blank=True)  # vitamin, flavor, garam, dll
    specs = models.JSONField(default=dict, blank=True)     # target SMP/IV atau work order
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.batch_code})"
