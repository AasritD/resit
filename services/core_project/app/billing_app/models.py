# services/core_project/app/billing_app/models.py

from django.db import models
from django.conf import settings
from django.urls import reverse


class UsageRecord(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    endpoint = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.user.username} - {self.endpoint} @ {self.timestamp}"


class Invoice(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    period_start = models.DateField()
    period_end = models.DateField()
    total_calls = models.IntegerField()
    amount_due = models.DecimalField(max_digits=8, decimal_places=2)
    generated_at = models.DateTimeField(auto_now_add=True)

    def get_pdf_url(self):
        # Make sure in urls.py you have:
        # app_name = 'billing_app'
        # and a path named 'invoice-pdf' that takes 'pk' as kwarg.
        return reverse('billing_app:invoice-pdf', kwargs={'pk': self.pk})

    def __str__(self):
        return f"Invoice #{self.pk} for {self.user.username}"
