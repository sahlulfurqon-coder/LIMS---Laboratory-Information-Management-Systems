from django.db import models
from django.conf import settings
from django.utils import timezone

# pilihan tank (storage J2–J13 and production TA–TF)
STORAGE_TANKS = [(f"J{i}", f"J{i}") for i in range(2, 14)]
PROD_TANKS = [("TA","TA"),("TB","TB"),("TC","TC"),("TD","TD"),("TE","TE"),("TF","TF")]
TANK_CHOICES = STORAGE_TANKS + PROD_TANKS

LINE_CHOICES = [
    ("A","Line A"),("B","Line B"),("C","Line C"),("D","Line D"),
    ("E","Line E"),("W","Line W"),("Y","Line Y"),("Z","Line Z")
]

SAMPLE_TYPE_CHOICES = [
    ("raw_material","Raw Material"),
    ("fatblend","Fat Blend"),
    ("finished_product","Finished Product"),
    ("packaging","Packaging"),
]

SAMPLE_STATUS = [
    ("REGISTERED","Registered"),
    ("IN_ANALYSIS","In Analysis"),
    ("IN_APPROVAL","In Approval"),
    ("APPROVED","Approved"),
    ("REJECTED","Rejected"),
    ("DELETED","Deleted"),
]

class SampleType(models.Model):
    code = models.CharField(max_length=64, unique=True)
    name = models.CharField(max_length=128)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


class RawMaterial(models.Model):
    """Master list of raw material oils (Olein, Stearin, SPMF, RBD PO, RCNO, ...)."""
    name = models.CharField(max_length=128, unique=True)
    description = models.TextField(blank=True, null=True)
    editable = models.BooleanField(default=False)  # master entries seeded non-editable by default

    def __str__(self):
        return self.name


class Packaging(models.Model):
    name = models.CharField(max_length=128, unique=True)
    description = models.TextField(blank=True, null=True)
    subtype = models.CharField(max_length=64, blank=True, null=True)  # e.g. PE, PP, PET or 'Carton Paper'
    editable = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Tank(models.Model):
    """
    Represents both storage tanks (J2..J13) and production tanks (TA..TF).
    For production tanks we track the current transfer that filled the tank.
    """
    code = models.CharField(max_length=8, choices=TANK_CHOICES, unique=True)
    capacity = models.DecimalField(max_digits=12, decimal_places=3, null=True, blank=True)
    current_transfer = models.ForeignKey("TransferRawMaterial", on_delete=models.SET_NULL, null=True, blank=True, related_name="filled_tank")

    def __str__(self):
        return self.code


class TransferRawMaterial(models.Model):
    """Event: transfer material from storage Tank(J) to production Tank(TA..TF)."""
    from_tank = models.CharField(max_length=8, choices=STORAGE_TANKS)
    to_tank = models.CharField(max_length=8, choices=PROD_TANKS)
    raw_material = models.ForeignKey(RawMaterial, on_delete=models.PROTECT)
    transfer_date = models.DateField(default=timezone.now)
    transfer_no = models.PositiveIntegerField(default=1)  # incrementing per to_tank per date business rule
    volume = models.DecimalField(max_digits=12, decimal_places=3, null=True, blank=True)
    requested_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name="transfer_requests")
    requested_at = models.DateTimeField(auto_now_add=True)
    approved_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name="transfer_approvals")
    approved_at = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=[('REQUESTED','Requested'),('APPROVED','Approved'),('REJECTED','Rejected'),('CANCELLED','Cancelled')], default='REQUESTED')
    notes = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ["-transfer_date","-transfer_no"]

    def sample_code(self):
        """Generate sample code like TA1180925 (to_tank + transfer_no + ddmmyy)."""
        dd = self.transfer_date.strftime("%d%m%y")
        return f"{self.to_tank}{self.transfer_no}{dd}"

    def __str__(self):
        return f"{self.raw_material} {self.from_tank}->{self.to_tank} ({self.transfer_date})"


class FatBlend(models.Model):
    code = models.CharField(max_length=64, unique=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name="created_fatblends")
    created_at = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.code}"


class FatBlendComponent(models.Model):
    fatblend = models.ForeignKey(FatBlend, on_delete=models.CASCADE, related_name="components")
    tank = models.ForeignKey(Tank, on_delete=models.PROTECT)  # link to production tank TA..TF
    percentage = models.DecimalField(max_digits=5, decimal_places=2)

    class Meta:
        unique_together = ("fatblend","tank")

    def __str__(self):
        return f"{self.fatblend.code}: {self.tank.code} ({self.percentage}%)"


class FinishedProduct(models.Model):
    name = models.CharField(max_length=128)
    batch_code = models.CharField(max_length=64, unique=True)
    production_code = models.CharField(max_length=64, blank=True, null=True)
    line = models.CharField(max_length=4, choices=LINE_CHOICES, blank=True, null=True)
    fatblend = models.ForeignKey(FatBlend, on_delete=models.SET_NULL, null=True, blank=True)
    packaging = models.ForeignKey(Packaging, on_delete=models.SET_NULL, null=True, blank=True)
    additives = models.JSONField(default=dict, blank=True)
    specs = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.batch_code})"


class Sample(models.Model):
    code = models.CharField(max_length=64, unique=True)
    sample_type = models.CharField(max_length=32, choices=SAMPLE_TYPE_CHOICES)
    reference_id = models.PositiveIntegerField(null=True, blank=True)  # polymorphic reference (id in other table)
    registered_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name="registered_samples")
    registered_at = models.DateTimeField(auto_now_add=True)
    received_at = models.DateTimeField(null=True, blank=True)
    urgency = models.CharField(max_length=20, choices=[("normal","Normal"),("urgent","Urgent")], default="normal")
    status = models.CharField(max_length=20, choices=SAMPLE_STATUS, default="REGISTERED")
    notes = models.TextField(blank=True, null=True)
    raw_meta = models.JSONField(default=dict, blank=True)

    approved_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name="approved_samples")
    approval_note = models.TextField(blank=True, null=True)
    approved_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ["-registered_at"]

    def __str__(self):
        return f"{self.code} ({self.get_sample_type_display()})"
