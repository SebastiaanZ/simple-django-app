FROM python:3.9.4-slim-buster as base

RUN useradd --system --shell /bin/false --uid 1500 app_user \
  && mkdir -p /app/staticfiles \
  && chown -R app_user /app/staticfiles \
  && pip install poetry==1.1.5

WORKDIR /app/simple_django_app

# Copy and install the dependencies first to
# avoid a cache miss if files unrelated to
# depencencies have changed.
COPY ["poetry.lock", "pyproject.toml", "./"]
ARG DEV=false
RUN poetry config virtualenvs.create false \
  && poetry install $(test "$DEV" != true && echo "--no-dev") \
     --no-interaction --no-ansi --no-root

# Now copy everything
COPY . .

# Switch to an unprivileged user
USER app_user
ENTRYPOINT ["python", "manage.py"]
CMD ["runserver", "0.0.0.0:8080"]

# ----------------------------------------------------------------------
FROM base as deploy
# This second stage is only needed for production
# environments that require a WSGI-server. For dev
# builds, `target=base` can be used.

USER root
RUN chmod +x ./entrypoint.sh

USER app_user
ENTRYPOINT ["./entrypoint.sh"]
