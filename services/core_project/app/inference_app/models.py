from django.db import models
from django.conf import settings

class ModelArtifact(models.Model):
    name        = models.CharField(max_length=100)
    version     = models.CharField(max_length=20)
    file        = models.FileField(upload_to='models/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    active      = models.BooleanField(default=False)  # mark which artifact is in use

    def __str__(self):
        return f"{self.name} v{self.version}"

class InferenceLog(models.Model):
    user        = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    model       = models.ForeignKey(ModelArtifact, on_delete=models.SET_NULL, null=True)
    input_file  = models.FileField(upload_to='inference_inputs/')
    prediction  = models.TextField()
    shap_values = models.JSONField(null=True, blank=True)
    created_at  = models.DateTimeField(auto_now_add=True)
    active      = models.BooleanField(default=False)
    def __str__(self):
        return f"Inference by {self.user.username} on {self.created_at}"
