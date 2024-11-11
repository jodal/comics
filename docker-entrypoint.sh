#!/bin/bash
set -e

# Simplified entrypoints for the different services packaged in this
# Docker image.

if [ "$1" = "shell" ]; then
    poetry run pip install ipython
    exec poetry run python manage.py shell ${*:2}
fi

if [ "$1" = "migrate" ]; then
    exec poetry run python manage.py migrate ${*:2}
fi

if [ "$1" = "web" ]; then
    exec poetry run gunicorn --worker-tmp-dir=/dev/shm --log-file=- --bind=0.0.0.0:$PORT comics.wsgi ${*:2}
fi

exec "$@"
