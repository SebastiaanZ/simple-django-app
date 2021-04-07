"""App configuration for our Blog application."""
from django.apps import AppConfig


class BlogConfig(AppConfig):
    """
    Blog configuration class.

    Note: `name` needs to be a fully qualified importable
    path to this module.
    """

    default_auto_field = "django.db.models.BigAutoField"
    name = "simple_django_app.blog"
    verbose_name = "A simple Django-backed blog."
