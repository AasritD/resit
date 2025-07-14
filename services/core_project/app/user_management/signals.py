# services/core_project/app/user_management/signals.py

from django.conf import settings
from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import ActivityLog
'''from inference_app.models import InferenceLog
from billing_app.models import BillableEvent'''

@receiver(user_logged_in)
def log_login(sender, user, request, **kwargs):
    ActivityLog.objects.create(user=user, action="login")

@receiver(user_logged_out)
def log_logout(sender, user, request, **kwargs):
    ActivityLog.objects.create(user=user, action="logout")

@receiver(post_save, sender=InferenceLog)
def log_inference(sender, instance, created, **kwargs):
    if created:
        ActivityLog.objects.create(
            user=instance.user,
            action=f"inference: {instance.prediction}"
        )

@receiver(post_save, sender=BillableEvent)
def log_billing(sender, instance, created, **kwargs):
    if created:
        ActivityLog.objects.create(
            user=instance.user,
            action=f"billing event: {instance.event_type}"
        )
