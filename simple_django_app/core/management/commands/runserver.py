"""
A module with a custom `runserver` command.

This command allows us to run a development server within a Docker
container by running some options automatically.
"""

import logging
import os

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.staticfiles.management.commands import runserver
from django.core import management
from django.core.management import CommandParser

log = logging.getLogger("college53.core.runserver")

SUPERUSER_WARNING_NON_DEBUG_MODE = (
    "A DEBUG superuser account will only be created in DEBUG mode. "
    "As DEBUG=False, no superuser account was created. "
    "Use the `--no-superuser` option to prevent this warning."
)


def create_debug_superuser() -> None:
    """Create a a superuser for debugging purposes."""
    user_model = get_user_model()
    admin_username = os.environ.get("ADMIN_USERNAME", "admin")
    admin_password = os.environ.get("ADMIN_PASSWORD", "admin")

    if not user_model.objects.filter(username=admin_username).exists():
        user = user_model.objects.create_superuser(
            username=admin_username,
            email="admin@admin.local",
            password=admin_password,
        )
        log.info("Created a superuser account with the username `%s`.", user.username)
    else:
        log.info("An account with the username `%s` already exists.", admin_username)


class Command(runserver.Command):
    """A custom runserver-command based on Django's runserver."""

    def add_arguments(self, parser: CommandParser) -> None:
        """Add arguments related to the `wait_for_postgres` function."""
        super().add_arguments(parser)
        parser.add_argument(
            "--no-superuser",
            action="store_false",
            dest="superuser",
            help="Tells Django to NOT create a superuser account.",
        )
        parser.add_argument(
            "--skip-migrations",
            action="store_false",
            dest="migrate",
            help="Tells Django to SKIP running migrations.",
        )
        parser.add_argument(
            "--no-collectstatic",
            action="store_false",
            dest="collectstatic",
            help="Tells Django to SKIP running collectstatic.",
        )

    def handle(self, *args, **options) -> None:
        """Handle the introduced functionality before running base handler."""
        # Only run these steps during the initial start-up procedure,
        # when RUN_MAIN is not yet set, not every time the file watcher
        # triggers an automatic reload.
        if not os.environ.get("RUN_MAIN", False):
            # Wait for the database to become available
            management.call_command("waitforpostgres")

            if options.pop("collectstatic", True):
                management.call_command("collectstatic", verbosity=1, interactive=False)

            if options.pop("migrate", True):
                management.call_command("migrate", verbosity=1, interactive=False)

            if options.pop("superuser", True):
                if not settings.DEBUG:
                    log.warning(SUPERUSER_WARNING_NON_DEBUG_MODE)
                else:
                    create_debug_superuser()

        super().handle(*args, **options)
