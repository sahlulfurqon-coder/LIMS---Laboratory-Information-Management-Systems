# lims_backend/accounts/permissions.py
from rest_framework import permissions

class IsAdmin(permissions.BasePermission):
    """
    Hanya user dengan role 'admin' atau superuser yang boleh.
    """
    def has_permission(self, request, view):
        user = request.user
        return bool(user and user.is_authenticated and (user.is_superuser or getattr(user, 'role', None) == 'admin'))

class IsAdminOrQAManager(permissions.BasePermission):
    """
    Admin atau QA Manager dapat mengakses endpoint tertentu (mis. list users).
    """
    def has_permission(self, request, view):
        user = request.user
        return bool(user and user.is_authenticated and (user.is_superuser or getattr(user,'role',None) in ['admin','qa_manager']))
