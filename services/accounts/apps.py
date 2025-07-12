from django.apps import AppConfig

class AuthServiceConfig(AppConfig):
    """
    AppConfig for the custom authentication service.
    The `label` must not collide with Django's built-in 'auth'.
    """
    name = 'services.auth'     # Python package path
    label = 'auth_service'     # Unique app label
    verbose_name = "Authentication Service"
