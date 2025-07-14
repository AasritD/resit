# services/core_project/app/user_management/admin.py

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin

from .models import CustomUser, ActivityLog
from inference_app.models import InferenceLog
from billing_app.models import UsageRecord


class InferenceLogInline(admin.TabularInline):
    model = InferenceLog
    extra = 0
    readonly_fields = ('input_file', 'prediction', 'created_at')


class UsageRecordInline(admin.TabularInline):
    model = UsageRecord
    extra = 0
    readonly_fields = ('endpoint', 'timestamp')


@admin.register(CustomUser)
class CustomUserAdmin(DjangoUserAdmin):
    list_display  = ('username', 'email', 'role', 'is_staff', 'is_active')
    list_filter   = ('role', 'is_staff', 'is_active')
    search_fields = ('username', 'email')
    fieldsets     = DjangoUserAdmin.fieldsets + (
        ('Role & Profile', {'fields': ('role',)}),
    )
    add_fieldsets = DjangoUserAdmin.add_fieldsets + (
        ('Role & Profile', {'fields': ('role',)}),
    )
    inlines       = [InferenceLogInline, UsageRecordInline]


@admin.register(ActivityLog)
class ActivityLogAdmin(admin.ModelAdmin):
    list_display  = ('timestamp', 'user', 'action')
    list_filter   = ('action', 'user__role')
    search_fields = ('user__username', 'action')
