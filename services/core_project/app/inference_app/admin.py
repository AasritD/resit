# services/inference/app/inference_app/admin.py

from django.contrib import admin
from .models import ModelArtifact, InferenceLog

@admin.register(ModelArtifact)
class ModelArtifactAdmin(admin.ModelAdmin):
    list_display = ('name', 'version', 'active', 'uploaded_at')
    list_filter  = ('active',)
    actions      = ['set_active']

    def set_active(self, request, queryset):
        # Deactivate all others first
        ModelArtifact.objects.update(active=False)
        # Then mark selected
        queryset.update(active=True)
    set_active.short_description = "Set selected artifacts as active"

@admin.register(InferenceLog)
class InferenceLogAdmin(admin.ModelAdmin):
    list_display     = ('user', 'model', 'created_at')
    readonly_fields  = ('input_file', 'prediction', 'shap_values', 'created_at')
    list_filter      = ('model', 'user')
    search_fields    = ('user__username', 'prediction')
