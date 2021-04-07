# A simple Django application
A simple Django application using class-based views.

## Running this project

Assuming you have Docker and docker-compose installed on your system, you can run a development server using:

```bash
docker-compose up
```

This will spin up a development server that should be accessible on `127.0.0.1:8080` in your browser. The local directory will be mapped the project directory within the container, meaning that Django's development server automatically reloads files if you make changes without requiring a rebuild of the container.
