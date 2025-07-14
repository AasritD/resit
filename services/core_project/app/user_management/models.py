# services/core_project/app/user_management/models.py

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings

class CustomUser(AbstractUser):
    class Roles(models.TextChoices):
        ENDUSER      = 'enduser',      'End User'
        AIENGINEER   = 'aiengineer',   'AI Engineer'
        ADMIN        = 'admin',        'Admin'
        FINANCE      = 'finance',      'Finance'

    role = models.CharField(
        max_length=20,
        choices=Roles.choices,
        default=Roles.ENDUSER,
    )

    def is_enduser(self):
        return self.role == self.Roles.ENDUSER

    def is_engineer(self):
        return self.role == self.Roles.AIENGINEER

    def is_admin(self):
        return self.role == self.Roles.ADMIN

    def is_finance(self):
        return self.role == self.Roles.FINANCE


class ActivityLog(models.Model):
    user      = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    action    = models.CharField(max_length=100)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.timestamp}: {self.user} – {self.action}"
