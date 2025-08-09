**********
Deployment
**********

The following example documents *one way* to deploy Comics. As Comics is a
standard Django project with an additional batch job for crawling, it may be
deployed in just about any way a Django project may be deployed. Please refer
to `Django's deployment documentation
<https://docs.djangoproject.com/en/dev/howto/deployment/>`_ for further
details.

In the following examples we assume that we are deploying Comics at
http://comics.example.com/, using Nginx, Gunicorn, and PostgreSQL. The Django
application and batch job is both running as the user ``comics-user``. The
static media files, like comic images, are served from
http://comics.example.com/static/.


Database
========

Comics should theoretically work with any database supported by Django.
Though, development is mostly done on SQLite and PostgreSQL. For production
use, PostgreSQL is the recommended choice.

.. note::

    If you are going to use SQLite in a deployment with Nginx and so on, you
    need to ensure that the user the web server will be running as has write
    access to the *directory* the SQLite database file is located in.


Example ``.env``
================

In the following examples, we assume the Comics source code is unpacked at
``/srv/comics.example.com/app``.

To change settings, you should not change the settings files shipped with
Comics, but instead override the settings using environment variables, or by
creating a file named ``/srv/comics.example.com/app/.env``. You must
at least set ``DJANGO_SECRET_KEY`` and database settings, unless you use
SQLite.

A full set of environment variables for a production deployment may look like
this:

.. code-block:: text

    DJANGO_SECRET_KEY=replace-this-with-a-long-random-value
    DJANGO_CSRF_TRUSTED_ORIGINS=https://comics.example.com

    DJANGO_DEFAULT_FROM_EMAIL=comics@example.com
    # Sending email, alternative 1: Using a local SMTP server
    DJANGO_EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
    # Sending email, alternative 2: Using the Mailgun API (which has a free tier)
    MAILGUN_API_KEY=your-mailgun-api-key

    DJANGO_MEDIA_ROOT=/srv/comics.example.com/htdocs/media/
    DJANGO_MEDIA_URL=https://comics.example.com/media/
    DJANGO_STATIC_ROOT=/srv/comics.example.com/htdocs/static/
    DJANGO_STATIC_URL=https://comics.example.com/static/

    DATABASE_URL=postgres://comics:topsecret-password@localhost:5432/comics

    CACHE_URL=memcache://127.0.0.1:11211

    COMICS_LOG_FILENAME=/srv/comics.example.com/log/comics.log
    COMICS_SITE_TITLE=comics.example.com
    COMICS_INVITE_MODE=true

Of course, you should change most, if not all, of these settings to fit your own
installation.

If your are not running a ``memcached`` server, remove ``CACHE_URL`` variable
from your environment. Comics does not require a cache, but responses are
significantly faster with a cache available.


Example Gunicorn setup
======================

Comics is a WSGI app and can be run with any WSGI server, for example
Gunicorn. Gunicorn is a Python program, so you can simply install it in
Comics' own virtualenv:

.. code-block:: sh

    cd /srv/comics.example.com/app
    uv sync --extra server

Then you need to start Gunicorn, for example with a systemd service:

.. code-block:: ini

    [Unit]
    Description=comics
    After=network.target

    [Install]
    WantedBy=multi-user.target

    [Service]
    User=comics-user
    Group=comics-user
    Restart=always

    WorkingDirectory=/srv/comics.example.com/app
    ExecStart=uv run gunicorn --bind=127.0.0.1:8000 --workers=9 --access-logfile=/srv/comics.example.com/htlogs/gunicorn-access.log --error-logfile=/srv/comics.example.com/htlogs/gunicorn-error.log comics.wsgi
    ExecReload=/bin/kill -s HUP $MAINPID
    ExecStop=/bin/kill -s TERM $MAINPID

    PrivateTmp=true


Example Nginx vhost
===================

The web server Nginx can be used in front of Gunicorn to terminate HTTPS
connections and effectively serve static files.

The following is an example of a complete Nginx vhost:

.. code-block:: nginx

    server {
        server_name comics.example.com;
        listen 443 ssl http2;
        listen [::]:443 ssl http2;

        access_log /srv/comics.example.com/htlogs/nginx-access.log;
        error_log /srv/comics.example.com/htlogs/nginx-error.log error;

        ssl_certificate /etc/letsencrypt/live/comics.example.com/fullchain.pem;
        ssl_certificate_key /etc/letsencrypt/live/comics.example.com/privkey.pem;

        location /media {
            root /srv/comics.example.com/htdocs;
            expires max;
        }

        location /static {
            root /srv/comics.example.com/htdocs;
            expires max;

            location ~* \/fonts\/ {
                add_header Access-Control-Allow-Origin *;
            }
        }

        location / {
            proxy_pass_header Server;
            proxy_set_header Host $http_host;
            proxy_redirect off;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
            proxy_set_header X-Scheme $scheme;
            proxy_connect_timeout 10;
            proxy_read_timeout 30;
            proxy_pass http://localhost:8000/;
        }
    }

For details, please refer to the documentation of the `Nginx
<http://nginx.org/en/docs/>`_ project.


.. _collecting-static-files:

Collecting static files
=======================

When you're not running in development mode, you'll need to collect the static
files from all apps into the ``STATIC_ROOT``. To do this, run::

    uv run comics collectstatic

You have to rerun this command every time you deploy changes to graphics, CSS
and JavaScript. For more details, see the Django documentation on `staticfiles
<https://docs.djangoproject.com/en/1.11/howto/static-files/>`_.


Example cronjob
===============

To get new comics releases, you should run ``get_releases`` regularly. In
addition, you should run ``clearsessions`` to clear expired user sessions.
One way is to use ``cron`` e.g. by placing the following in
``/etc/cron.d/comics``:

.. code-block:: sh

    MAILTO=comics@example.com
    PYTHONPATH=/srv/comics.example.com/app/comics
    1 * * * * comics-user cd /srv/comics.example.com/app && uv run comics get_releases -v0
    1 3 * * * comics-user cd /srv/comics.example.com/app && uv run comics clearsessions -v0

By setting ``MAILTO`` any exceptions raised by the comic crawlers will be sent
by mail to the given mail address. ``1 * * * *`` specifies that the command
should be run 1 minute past every hour.
