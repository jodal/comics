#!/bin/bash
set -e

# Simplified entrypoints for the different services packaged in this
# Docker image.

if [ "$1" = "shell" ]; then
    exec comics shell ${*:2}
fi

if [ "$1" = "dbshell" ]; then
    exec comics dbshell ${*:2}
fi

if [ "$1" = "web" ]; then
    comics migrate
    # Media files are served by Granian itself, without involving the Python
    # app. Since media file names contain the file's checksum, they can be
    # cached forever.
    exec granian \
        --interface wsgi \
        --host 0.0.0.0 \
        --port ${PORT:-8000} \
        --static-path-route /media \
        --static-path-mount ${DJANGO_MEDIA_ROOT:-/media} \
        --static-path-expires 31536000 \
        ${*:2} \
        comics.wsgi:application
fi

exec "$@"
