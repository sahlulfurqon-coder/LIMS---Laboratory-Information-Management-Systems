# lims_backend/accounts/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ROLE_QA_MANAGER = "qa_manager"
    ROLE_QA_SUPERVISOR = "qa_supervisor"
    ROLE_RND = "rnd"
    ROLE_ANALYST = "analyst"

    ROLE_CHOICES = [
        (ROLE_QA_MANAGER, "QA Manager"),
        (ROLE_QA_SUPERVISOR, "QA Supervisor"),
        (ROLE_RND, "RnD"),
        (ROLE_ANALYST, "Analyst"),
    ]

    role = models.CharField(
        max_length=32,
        choices=ROLE_CHOICES,
        blank=True,
        null=True,   # <-- role biar boleh kosong
    )

    phone = models.CharField(max_length=32, blank=True, null=True)
    department = models.CharField(max_length=128, blank=True, null=True)

    def is_admin(self):
        """Superuser selalu dianggap admin teknis"""
        return self.is_superuser

    def __str__(self):
        return f"{self.username} ({'Superuser' if self.is_superuser else self.get_role_display()})"

    @property
    def role_display(self):
        if self.is_superuser:
            return "Superuser"
        if self.is_staff and not self.role:
            return "Staff"
        return self.get_role_display() if self.role else "-"