from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    # Add 'role' to admin display
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Role & Permissions', {'fields': ('role',)}),
    )
    list_display = ['username', 'email', 'role', 'is_active', 'is_staff']
    list_filter = ['role', 'is_active', 'is_staff']
