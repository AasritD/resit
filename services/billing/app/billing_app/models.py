from django.db import models
from django.contrib.auth.models import User

class UsageRecord(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    endpoint = models.CharField(max_length=100)

class Invoice(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    period_start = models.DateField()
    period_end = models.DateField()
    total_calls = models.IntegerField()
    amount_due = models.DecimalField(max_digits=8,decimal_places=2)
    generated_at = models.DateTimeField(auto_now_add=True)
