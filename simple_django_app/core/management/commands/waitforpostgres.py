"""
A module that provides a manage.py command to wait for a database.

Our Django-application can only start once our database server accepts
incoming connections. Since we cannot always guarantee start-up order
in container-based deployment and development environments, the custom
manage.py command provided by this module waits for the database to
become available, with incremental back-off logic.
"""
import argparse
import logging
import os
import time

import psycopg2
from django.core.management import BaseCommand

log = logging.getLogger("simple_django_app.core.waitforpostgres")


def wait_for_postgres(max_attempts: int = 5, backoff_exponent: int = 1) -> None:
    """Wait for Postgres to be ready to accept connections."""
    log.info("Waiting for database to start up.")
    for attempt in range(1, max_attempts + 1):
        try:
            log.info("Attempting to connect to database [%s/%s]", attempt, max_attempts)
            conn = psycopg2.connect(os.environ["DATABASE_URL"])
        except psycopg2.OperationalError:
            if attempt < max_attempts:
                delay = attempt ** backoff_exponent
                log.info("Connection failed, sleeping for %s second...", delay)
                time.sleep(delay)
            else:
                log.critical("Failed to connect to database.")
                raise
        else:
            log.info("Connected successfully to the database.")
            conn.close()
            break


class Command(BaseCommand):
    """A command to wait for postgres to become available."""

    def add_arguments(self, parser: argparse.ArgumentParser) -> None:
        """Add additional arguments to the default argument parser."""
        super().add_arguments(parser)
        parser.add_argument(
            "--database-attempts",
            action="store",
            type=int,
            default=5,
            dest="max_database_attempts",
            help="Maximum number of database connection attempts that are made (default=5).",
        )
        parser.add_argument(
            "--exponential-backoff",
            action="store",
            type=int,
            default=1,
            dest="backoff_exponent",
            help="Exponent applied to the incremental back-offs (default=1).",
        )

    def handle(self, *args, **options) -> None:
        """Handle the command line options and execute the waiter."""
        max_database_attempts = options.pop("max_database_attempts", 5)
        backoff_exponent = options.pop("backoff_exponent", 1)
        wait_for_postgres(max_database_attempts, backoff_exponent)
