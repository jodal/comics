FROM python:3.12.3-slim-bookwor

ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONUNBUFFERED=1

# Install system dependencies
RUN apt-get update \
    && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Create app user
RUN groupadd app \
    && useradd -g app -d /home/app -s /sbin/nologin app \
    && mkdir -p /home/app \
    && chown -R app:app /home/app

# Create app directory
RUN mkdir /app \
    && chown -R app:app /app

# Install system dependencies
RUN pip install --no-cache poetry==1.8.2

# Add app directory to Python path
ENV PYTHONPATH=/app

# Activate app user and change working directory
USER app
WORKDIR /app

# Install app dependencies
COPY --chown=app ./pyproject.toml ./poetry.toml ./poetry.lock /app/
RUN poetry install \
    --no-root --no-dev --no-interaction --no-ansi \
    --extras api \
    --extras cache \
    --extras pgsql \
    --extras server

# Install app
COPY --chown=app ./docker-entrypoint.sh /app/
COPY --chown=app ./manage.py /app/
COPY --chown=app ./comics/ /app/comics/

# Collect static files
RUN DJANGO_SECRET_KEY=s3cret poetry run python manage.py collectstatic --noinput

# Entrypoint
ENTRYPOINT ["./docker-entrypoint.sh"]
