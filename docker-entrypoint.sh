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
    exec granian \
        --interface wsgi \
        --host 0.0.0.0 \
        --port ${PORT:-8000} \
        ${*:2} \
        comics.wsgi:application
fi

exec "$@"
