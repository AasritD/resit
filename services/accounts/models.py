from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ROLE_CUSTOMER   = 'customer'
    ROLE_ADMIN      = 'admin'
    ROLE_SUPERADMIN = 'super'

    ROLE_CHOICES = [
        (ROLE_CUSTOMER,   'Customer'),
        (ROLE_ADMIN,      'Admin'),
        (ROLE_SUPERADMIN, 'SuperAdmin'),
    ]

    role = models.CharField(
        max_length=10,
        choices=ROLE_CHOICES,
        default=ROLE_CUSTOMER,
        help_text="Defines the user's access level"
    )

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"
