from rest_framework import serializers
from .models import UsageRecord, Invoice

class UsageRecordSerializer(serializers.ModelSerializer):
    class Meta: model=UsageRecord; fields='__all__'

class InvoiceSerializer(serializers.ModelSerializer):
    class Meta: model=Invoice; fields='__all__'
