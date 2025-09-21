# lims_backend/accounts/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ROLE_ADMIN = 'admin'
    ROLE_QA_MANAGER = 'qa_manager'
    ROLE_QA_SUPERVISOR = 'qa_supervisor'
    ROLE_RND = 'rnd'
    ROLE_ANALYST = 'analyst'

    ROLE_CHOICES = [
        (ROLE_ADMIN, 'Admin'),
        (ROLE_QA_MANAGER, 'QA Manager'),
        (ROLE_QA_SUPERVISOR, 'QA Supervisor'),
        (ROLE_RND, 'RnD'),
        (ROLE_ANALYST, 'Analyst'),
    ]

    role = models.CharField(max_length=32, choices=ROLE_CHOICES, default=ROLE_ANALYST)
    phone = models.CharField(max_length=32, blank=True, null=True)
    department = models.CharField(max_length=128, blank=True, null=True)
    # jika perlu: is_active sudah ada di AbstractUser
    # created_at otomatis di AbstractUser via date_joined

    def is_admin(self):
        return self.role == self.ROLE_ADMIN or self.is_superuser

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"
