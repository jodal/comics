**********
Deployment
**********

Comics is a standard Django project plus a batch job for crawling comics, so it
can be deployed in just about any way a Django project can. This guide documents
*one* modern setup: running the published container image with **rootless
Podman**, behind **Caddy**, using a **PostgreSQL** server on the host, and
keeping the **media library on the host filesystem**.

For other approaches, please refer to `Django's deployment documentation
<https://docs.djangoproject.com/en/dev/howto/deployment/>`_.


Architecture
============

The pieces fit together like this:

- **Caddy** terminates HTTPS, serves ``/media/`` directly from the host disk,
  and reverse-proxies everything else to the app container.
- The **app container** runs Gunicorn (the image's ``web`` entrypoint) as a
  rootless Podman container owned by a dedicated, unprivileged host user.
- **PostgreSQL** keeps running on the host, unchanged.
- The **media library** stays on the host filesystem and is bind-mounted into
  the container.

The container itself is **stateless**: the database lives on the host, media
lives on the host, and static files are collected into the image at build time
and served by WhiteNoise from inside the app. No Podman volumes are required.

Throughout we assume:

- The site is served at ``https://comics.example.com/``.
- A dedicated, unprivileged host user ``comics`` runs Podman.
- The media library lives at ``/srv/comics/media`` and is owned by ``comics``.
- Configuration lives in ``/home/comics/.config/comics/comics.env``.


Prerequisites
=============

Install Podman (4.4+ for Quadlet; 5.0+ recommended) and Caddy using your
distribution's packages.

Create the dedicated user and allow its services to run without an active login
session (``linger``), so the app and its timers start at boot:

.. code-block:: sh

    sudo useradd --create-home --system comics
    sudo loginctl enable-linger comics

Rootless Podman maps container UIDs through the host user's subordinate UID/GID
ranges. These are usually configured automatically; if not, add them:

.. code-block:: sh

    sudo usermod --add-subuids 100000-165535 --add-subgids 100000-165535 comics

Run the remaining commands as the ``comics`` user, for example via
``sudo machinectl shell comics@`` or ``sudo -iu comics``.


The image
=========

The image is built and published to the GitHub Container Registry by CI on every
successful build of the ``main`` branch, tagged with ``latest`` and the commit
SHA:

.. code-block:: sh

    podman pull ghcr.io/jodal/comics:latest


Configuration
=============

The app is configured entirely through environment variables. Put them in a file
readable only by the ``comics`` user:

.. code-block:: sh

    mkdir -p ~/.config/comics
    install -m 600 /dev/null ~/.config/comics/comics.env

A production ``comics.env`` may look like this:

.. code-block:: text

    # Generate once and keep stable; changing it logs everyone out and breaks
    # outstanding password-reset/invitation links.
    DJANGO_SECRET_KEY=replace-this-with-a-long-random-value

    DJANGO_ALLOWED_HOSTS=comics.example.com
    DJANGO_CSRF_TRUSTED_ORIGINS=https://comics.example.com

    # Caddy serves /media/ from disk; the URL stays relative to the site.
    DJANGO_MEDIA_URL=/media/

    # Existing host PostgreSQL, reached over Podman's host alias.
    DATABASE_URL=postgres://comics:topsecret-password@host.containers.internal:5432/comics

    DJANGO_DEFAULT_FROM_EMAIL=comics@example.com
    DJANGO_EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend

    # Optional: a cache makes responses significantly faster.
    CACHE_URL=memcache://host.containers.internal:11211

    # Optional: Sentry crash reporting.
    SENTRY_DSN=https://...

    COMICS_SITE_TITLE=comics.example.com
    COMICS_INVITE_MODE=true

.. note::

    Do **not** set ``DJANGO_STATIC_ROOT`` or ``DJANGO_MEDIA_ROOT`` here. The
    image already points them at ``/app/static`` (baked in at build time) and
    ``/media`` (the bind mount described below).

Generate a strong secret key with::

    podman run --rm ghcr.io/jodal/comics:latest \
        python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"


Database
========

We're using a PostgreSQL instance already running on the host. A rootless
container reaches the host through the ``host.containers.internal`` alias that
Podman adds automatically, so the ``DATABASE_URL`` above needs no special
networking.

Make sure PostgreSQL accepts the connection: it must listen on an address the
container can reach (binding only to ``localhost`` is not enough when you use the
host alias — bind it to the Podman bridge or the host's LAN address), and
``pg_hba.conf`` must allow the ``comics`` database user with password
(``scram-sha-256``/``md5``) authentication.

The ``web`` entrypoint runs ``comics migrate`` automatically on start, so schema
migrations are applied against the existing database whenever the container
starts.


Media on the host filesystem
============================

The image stores media at ``/media`` and runs as container UID ``1000``. To keep
the existing library on the host and have downloaded strips owned by the
``comics`` user, bind-mount the directory and map the host user onto the
container user with ``keep-id``:

.. code-block:: sh

    --userns=keep-id:uid=1000,gid=1000 \
    --volume=/srv/comics/media:/media:rw

Why ``keep-id``? In rootless Podman, container UID ``1000`` would otherwise map
to a high subordinate UID on the host — it could neither read your existing media
nor write files owned by ``comics``. ``keep-id:uid=1000,gid=1000`` maps the host
``comics`` user to container UID ``1000`` instead, so the existing library is
readable and writable and new files land owned by ``comics``.

Ensure the directory is owned by ``comics`` (do this once for the existing
library)::

    sudo chown -R comics:comics /srv/comics/media

Caddy runs as its own user and needs **read** access to the same directory. Grant
it via a shared group or an ACL, for example::

    sudo setfacl -R -m u:caddy:rX -m d:u:caddy:rX /srv/comics/media

.. note::

    On SELinux hosts (Fedora/RHEL) a bind mount also needs a relabel. Use the
    shared ``:z`` suffix — **not** ``:Z``, which applies a private label and
    would lock Caddy out of the shared media directory. On Debian/Ubuntu hosts
    (which use AppArmor) no relabel is needed.


Running the app with Podman (Quadlet)
=====================================

Manage the container as a systemd user service via a Podman *Quadlet* unit. As
the ``comics`` user, create
``~/.config/containers/systemd/comics-web.container``:

.. code-block:: ini

    [Unit]
    Description=Comics web app
    After=network-online.target
    Wants=network-online.target

    [Container]
    Image=ghcr.io/jodal/comics:latest
    AutoUpdate=registry

    # Map the host "comics" user onto the image's UID 1000.
    UserNS=keep-id:uid=1000,gid=1000

    # Keep the media library on the host disk.
    Volume=/srv/comics/media:/media:rw

    # Production settings.
    EnvironmentFile=%h/.config/comics/comics.env

    # Only Caddy needs to reach the app, so bind to loopback.
    PublishPort=127.0.0.1:8000:8000

    # Run Gunicorn (migrate + serve) with production worker tuning. Arguments
    # after "web" are passed through to Gunicorn.
    Exec=web --workers=9 --access-logfile=- --error-logfile=-

    [Service]
    Restart=always

    [Install]
    WantedBy=default.target

Then load and start it:

.. code-block:: sh

    systemctl --user daemon-reload
    systemctl --user start comics-web.service

Quadlet generates ``comics-web.service`` from the ``.container`` file; it starts
on boot thanks to ``WantedBy=default.target`` and the enabled linger.

If you want the host to pull and restart on new images published by CI, enable
auto-updates (this works together with ``AutoUpdate=registry`` above):

.. code-block:: sh

    systemctl --user enable --now podman-auto-update.timer


Caddy
=====

Caddy terminates HTTPS, serves media straight from disk, and proxies the rest to
the app. Static files are served by WhiteNoise from inside the app, so Caddy does
not need to handle ``/static/``.

.. code-block:: text

    comics.example.com {
        encode zstd gzip

        @media path /media/*
        handle @media {
            root * /srv/comics
            file_server
            header Cache-Control "public, max-age=31536000, immutable"
        }

        handle {
            reverse_proxy 127.0.0.1:8000
        }
    }

A request for ``/media/foo.png`` is served from ``/srv/comics/media/foo.png``
without touching the app.


Scheduled jobs
==============

To fetch new releases you must run ``get_releases`` regularly, and you should run
``clearsessions`` to purge expired sessions. Run each as a short-lived container
from a systemd user timer. Because the container is stateless, these reuse the
same image, env file, media mount, and ``keep-id`` mapping as the web service.

Create ``~/.config/systemd/user/comics-get-releases.service``:

.. code-block:: ini

    [Unit]
    Description=Fetch new comics releases

    [Service]
    Type=oneshot
    ExecStart=/usr/bin/podman run --rm \
        --userns=keep-id:uid=1000,gid=1000 \
        --volume=/srv/comics/media:/media:rw \
        --env-file=%h/.config/comics/comics.env \
        ghcr.io/jodal/comics:latest comics get_releases -v0

...and ``~/.config/systemd/user/comics-get-releases.timer``:

.. code-block:: ini

    [Unit]
    Description=Fetch new comics releases hourly

    [Timer]
    OnCalendar=hourly
    Persistent=true

    [Install]
    WantedBy=timers.target

Create the matching ``comics-clearsessions.service`` (running
``comics clearsessions -v0``) and a daily ``comics-clearsessions.timer``
(``OnCalendar=daily``).

Enable the timers:

.. code-block:: sh

    systemctl --user daemon-reload
    systemctl --user enable --now comics-get-releases.timer
    systemctl --user enable --now comics-clearsessions.timer

.. tip::

    Run a crawl on demand to verify the setup with
    ``systemctl --user start comics-get-releases.service`` and inspect the output
    with ``journalctl --user -u comics-get-releases.service``.
