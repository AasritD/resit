from rest_framework import serializers
from .models import ExperimentRun

class ExperimentRunSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExperimentRun
        fields = '__all__'
