FROM python:3.14.6-slim-trixie AS base

# --------------------------------------------

FROM base AS build
SHELL ["sh", "-exc"]

# Install uv (pinned for reproducible builds)
COPY --from=ghcr.io/astral-sh/uv:0.11.21 /uv /usr/local/bin/uv

# - Compile Python bytecode for faster app startup.
# - Silence uv complaining about not being able to use hard links.
# - Set the project virtualenv to /app.
# - Pick a Python.
# - Prevent uv from accidentally downloading isolated Python builds.
ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    UV_PROJECT_ENVIRONMENT=/app \
    UV_PYTHON=/usr/local/bin/python \
    UV_PYTHON_DOWNLOADS=never

# Install app dependencies
COPY pyproject.toml /_lock/
COPY uv.lock /_lock/
RUN --mount=type=cache,target=/root/.cache <<EOT
cd /_lock
uv sync \
    --locked \
    --no-dev \
    --all-extras \
    --no-install-project
EOT

# Install app
COPY . /src
RUN --mount=type=cache,target=/root/.cache <<EOT
cd /src
uv sync \
    --locked \
    --no-dev \
    --all-extras \
    --no-editable
EOT

# Collect static files
ENV DJANGO_STATIC_ROOT=/app/static
RUN <<EOT
/app/bin/comics collectstatic --noinput
/app/bin/comics compress
EOT

# --------------------------------------------

FROM base AS runtime
SHELL ["sh", "-exc"]

# Runtime system dependencies.
# psycopg (3) is installed without the bundled binary, so it needs the
# system libpq library to talk to PostgreSQL.
RUN <<EOT
apt-get update -qq
apt-get install -y --no-install-recommends libpq5
rm -rf /var/lib/apt/lists/*
EOT

# Put installed Python packages in PATH
ENV PATH=/app/bin:${PATH}

# Make GIT_SHA from build-args available in the container's environment
ARG GIT_SHA
ENV GIT_SHA=${GIT_SHA}

# OCI image metadata. CI's docker/metadata-action augments these with dynamic
# values (created, version) at publish time.
LABEL org.opencontainers.image.source="https://github.com/jodal/comics" \
      org.opencontainers.image.url="https://github.com/jodal/comics" \
      org.opencontainers.image.title="comics" \
      org.opencontainers.image.description="Comics is a webcomics aggregator." \
      org.opencontainers.image.licenses="AGPL-3.0-only" \
      org.opencontainers.image.revision="${GIT_SHA}"

# App settings
ENV DJANGO_STATIC_ROOT=/app/static
ENV DJANGO_MEDIA_ROOT=/media

# Create app user
RUN <<EOT
groupadd -g 1000 app
useradd -g 1000 -u 1000 -d /home/app -s /sbin/nologin app
mkdir -p /home/app
chown -R app:app /home/app
EOT

# Create app directory
RUN <<EOT
mkdir /app
chown -R app:app /app
EOT

# Entrypoint
COPY --chown=app:app ./docker-entrypoint.sh /
ENTRYPOINT ["/docker-entrypoint.sh"]

# Stop app with SIGINT (like Ctrl+C) instead of SIGTERM
STOPSIGNAL SIGINT

# Install app
COPY --from=build --chown=app:app /app /app

# Activate app user and change working directory
# Use UID for compatibility with K8s's securityContext.runAsNonRoot
USER 1000
WORKDIR /app

# Smoketest
RUN <<EOT
python -V
python -Im site
python -Ic 'import comics'
python -Ic 'import psycopg'
EOT
