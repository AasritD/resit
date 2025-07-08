from django.db import models
from django.contrib.auth.models import User

class ModelArtifact(models.Model):
    name = models.CharField(max_length=100)
    version = models.CharField(max_length=20)
    file = models.FileField(upload_to='models/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

class InferenceLog(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    model = models.ForeignKey(ModelArtifact,on_delete=models.SET_NULL,null=True)
    input_file = models.FileField(upload_to='inference_inputs/')
    prediction = models.TextField()
    shap_values = models.JSONField(null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
