# lims_backend/accounts/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from .models import User

@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    list_display = ('username','email','first_name','last_name','role','is_active','is_staff')
    list_filter = ('role','is_active','is_staff')
    fieldsets = (
        (None, {'fields': ('username','password')}),
        ('Personal info', {'fields': ('first_name','last_name','email','phone','department')}),
        ('Permissions', {'fields': ('is_active','is_staff','is_superuser','role','groups','user_permissions')}),
        ('Important dates', {'fields': ('last_login','date_joined')}),
    )
    search_fields = ('username','first_name','last_name','email')
    ordering = ('username',)
