from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('enduser', 'End User'),
        ('aiengineer', 'AI Engineer'),
        ('admin', 'Admin'),
        ('finance', 'Finance'),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='enduser')
