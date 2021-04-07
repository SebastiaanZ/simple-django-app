"""Configurations for our core application."""
from django.apps import AppConfig


class CoreConfig(AppConfig):
    """
    Configuration class for our core application.

    Note that `name` needs to be a fully qualified importable
    name.
    """

    default_auto_field = "django.db.models.BigAutoField"
    name = "simple_django_app.core"
