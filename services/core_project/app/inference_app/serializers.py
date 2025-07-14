from rest_framework import serializers
from .models import ModelArtifact, InferenceLog

class ModelArtifactSerializer(serializers.ModelSerializer):
    class Meta: model = ModelArtifact; fields = '__all__'

class InferenceLogSerializer(serializers.ModelSerializer):
    class Meta: model = InferenceLog; fields = '__all__'
