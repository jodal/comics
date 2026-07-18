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
- **PostgreSQL** runs on the host.
- The **media library** is on the host filesystem and is bind-mounted into the
  container.

The container itself is **stateless**: the database lives on the host, media
lives on the host, and static files are collected into the image at build time
and served by WhiteNoise from inside the app. No Podman volumes are required.

Throughout we assume:

- The site is served at ``https://comics.example.com/``.
- Everything related to the deployment lives under ``/srv/comics``.
- A dedicated, unprivileged host user ``comics`` runs Podman, with its home
  directory at ``/srv/comics/home``.
- The media library lives at ``/srv/comics/media`` and is owned by ``comics``.
- Configuration lives in ``/srv/comics/comics.env``.


Prerequisites
=============

Install Podman 5.0 or newer — this guide relies on *Quadlet* and on the *pasta*
network mode being the default, which it is since 5.0 — and Caddy, both from
your distribution's packages.

Create the dedicated user and allow its services to run without an active login
session (``linger``), so the app and its timers start at boot. The home
directory is placed under ``/srv/comics`` to keep the whole deployment —
configuration, systemd units, container storage, and the media library — in
one place:

.. code-block:: sh

    sudo useradd --create-home --home-dir /srv/comics/home --system comics
    sudo loginctl enable-linger comics

Since ``comics`` is a system user (UID below 1000), journald stores the logs of
its services in the *system* journal, which unprivileged users cannot read. Add
the user to the ``systemd-journal`` group so that the ``journalctl --user``
commands used throughout this guide work:

.. code-block:: sh

    sudo usermod -aG systemd-journal comics

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

The app is configured entirely through environment variables. Put them in a
file readable only by the ``comics`` user. Create it as root, since
``/srv/comics`` itself is owned by root:

.. code-block:: sh

    sudo install -m 600 -o comics -g comics /dev/null /srv/comics/comics.env

A production ``comics.env`` may look like this:

.. code-block:: text

    # Generate once and keep stable; changing it logs everyone out and breaks
    # outstanding password-reset/invitation links.
    DJANGO_SECRET_KEY=replace-this-with-a-long-random-value

    # Caddy serves /media/ from disk. Use an absolute URL so that comic
    # images work everywhere, including in Atom feed entries viewed in feed
    # readers.
    DJANGO_MEDIA_URL=https://comics.example.com/media/

    # Host PostgreSQL, reached via pasta port forwarding (see the "Host
    # services" section). Inside the container, 127.0.0.1:5432 is the host's
    # PostgreSQL.
    DATABASE_URL=postgres://comics:topsecret-password@127.0.0.1:5432/comics

    DJANGO_DEFAULT_FROM_EMAIL=comics@example.com

    # Sending email, alternative 1: Using the Mailgun API (which has a free
    # tier). If both alternatives are configured, Mailgun is used.
    MAILGUN_API_KEY=your-mailgun-api-key
    MAILGUN_API_URL=https://api.eu.mailgun.net/v3
    MAILGUN_SENDER_DOMAIN=comics.example.com

    # Sending email, alternative 2: Using an SMTP server. An SMTP server on
    # the container host is reached via pasta port forwarding, just like
    # PostgreSQL and memcached (see the "Host services" section). All settings
    # except the backend and host default to Django's defaults.
    DJANGO_EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
    DJANGO_EMAIL_HOST=127.0.0.1
    DJANGO_EMAIL_PORT=25
    DJANGO_EMAIL_HOST_USER=smtp-username
    DJANGO_EMAIL_HOST_PASSWORD=smtp-password
    DJANGO_EMAIL_USE_TLS=false
    DJANGO_EMAIL_USE_SSL=false

    # Optional: a cache makes responses significantly faster. Host memcached
    # is also reached via pasta port forwarding.
    CACHE_URL=memcache://127.0.0.1:11211

    # Optional: Sentry crash reporting.
    SENTRY_DSN=https://...

    # Base URL where the site is reachable. Used to build absolute URLs,
    # e.g. in Atom feeds, and as the default for the allowed hosts and CSRF
    # trusted origins (override with DJANGO_ALLOWED_HOSTS and
    # DJANGO_CSRF_TRUSTED_ORIGINS if they need to differ).
    COMICS_SITE_URL=https://comics.example.com

    COMICS_SITE_TITLE=comics.example.com
    COMICS_INVITE_MODE=true

.. note::

    Do **not** set ``DJANGO_STATIC_ROOT`` or ``DJANGO_MEDIA_ROOT`` here. The
    image already points them at ``/app/static`` (baked in at build time) and
    ``/media`` (the bind mount described below).

Generate a strong secret key with::

    podman run --rm ghcr.io/jodal/comics:latest \
        python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"


Host services
=============

PostgreSQL — and, if you use them, memcached and an SMTP server — runs on the
host and listens only on ``localhost``, as is common on a single server. The
container cannot reach them there directly: inside the container,
``127.0.0.1`` is the container itself.

Instead of exposing these services on a routable address, we use the port
forwarding built into *pasta*, rootless Podman's default network mode. Its
``-T`` option forwards connections that the container makes to given ports on
*its own* loopback to the same ports on the *host's* loopback. Both the web
service and the scheduled jobs below therefore run with::

    --network=pasta:-T,5432,-T,11211,-T,25

which forwards PostgreSQL (5432), memcached (11211), and SMTP (25). From inside
the container, these host services are simply ``127.0.0.1``, matching the URLs
in ``comics.env`` above. Forward only the ports you actually use.

The host services need no reconfiguration, and nothing new is exposed to the
network. To PostgreSQL, a connection from the container looks like any other
local connection from ``127.0.0.1``, so the standard ``pg_hba.conf`` rules for
``127.0.0.1/32`` apply: the ``comics`` database user must be allowed to connect
over TCP with password (``scram-sha-256``/``md5``) authentication — peer
authentication over the Unix socket is not available from inside the container.

If you are starting fresh rather than migrating an existing installation,
create the database user and the database first, with the same password as in
``DATABASE_URL``::

    sudo -u postgres createuser --pwprompt comics
    sudo -u postgres createdb --owner comics comics

The ``web`` entrypoint runs ``comics migrate`` automatically on start, so the
database schema is created and migrated whenever the container starts.


Media on the host filesystem
============================

The image stores media at ``/media`` and runs as container UID ``1000``. To keep
the existing library on the host and have downloaded strips owned by the
``comics`` user, bind-mount the host directory into the container and map the
host user onto the container user. Both the web service and the scheduled jobs
below apply this with two settings: ``--volume=/srv/comics/media:/media:rw``
mounts ``/srv/comics/media`` onto the container's ``/media``, and
``--userns=keep-id:uid=1000,gid=1000`` maps the host ``comics`` user onto
container UID ``1000``. You don't run these directly; they appear in the unit
files in the sections that follow.

Why ``keep-id``? In rootless Podman, container UID ``1000`` would otherwise map
to a high subordinate UID on the host — it could neither read your existing media
nor write files owned by ``comics``. ``keep-id:uid=1000,gid=1000`` maps the host
``comics`` user to container UID ``1000`` instead, so the existing library is
readable and writable and new files land owned by ``comics``.

Ensure the directory is owned by ``comics`` (do this once for the existing
library)::

    sudo chown -R comics:comics /srv/comics/media

Caddy runs as its own user and needs **read** access to the same directory.
With the container's default umask, downloaded strips land world-readable
(``644``), so this works out of the box. The rest of this section is only
needed if you want to keep the library private to ``comics`` and ``caddy``: add
the ``caddy`` user to the ``comics`` group, make the library group- but not
world-readable, and set the setgid bit (``g+s``) so new subdirectories inherit
the ``comics`` group::

    sudo usermod -aG comics caddy
    sudo chmod -R g+rX,o-rwx /srv/comics/media
    sudo find /srv/comics/media -type d -exec chmod g+s {} +

Restart Caddy afterwards so its new group membership takes effect. Also run the
containers with ``--umask=007`` (in the Quadlet unit: ``PodmanArgs=--umask=007``)
so that new strips land group- but not world-readable as well.


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
    EnvironmentFile=/srv/comics/comics.env

    # Forward container-loopback ports to the host's services (see the
    # "Host services" section).
    Network=pasta:-T,5432,-T,11211,-T,25

    # Only Caddy needs to reach the app, so bind to loopback.
    PublishPort=127.0.0.1:8000:8000

    # Run Gunicorn (migrate + serve). Arguments after "web" are passed through
    # to Gunicorn; size --workers to roughly 2 x CPU cores + 1.
    Exec=web --workers=9 --access-logfile=- --error-logfile=-

    [Service]
    Restart=always

    [Install]
    WantedBy=default.target

Then load and start it:

.. code-block:: sh

    systemctl --user daemon-reload
    systemctl --user start comics-web.service
    journalctl --user -u comics-web.service

The journal should show ``comics migrate`` running, followed by Gunicorn booting
its workers. Quadlet generates ``comics-web.service`` from the ``.container``
file; it starts on boot thanks to ``WantedBy=default.target`` and the enabled
linger.

If you want the host to pull and restart on new images published by CI, enable
auto-updates (this works together with ``AutoUpdate=registry`` above). This also
keeps the scheduled jobs below on fresh images: ``podman run`` uses the image
from local storage without pulling, so it is the auto-update timer that moves
``latest`` forward:

.. code-block:: sh

    systemctl --user enable --now podman-auto-update.timer

.. tip::

    ``podman auto-update`` can also be run by hand at any time to check for a
    new image and, if one is found, pull it and restart the web service
    immediately.


Caddy
=====

Caddy terminates HTTPS, serves media straight from disk, and proxies the rest to
the app. Static files are served by WhiteNoise from inside the app, so Caddy does
not need to handle ``/static/``.

The app trusts the ``X-Forwarded-Proto`` header to detect that a request
arrived over HTTPS. Caddy sets the header on every proxied request and ignores
any value sent by clients, so this works out of the box. If you use another
reverse proxy, make sure it does the same, or point the app at the right
header, e.g. ``DJANGO_SECURE_PROXY_SSL_HEADER=HTTP_X_FORWARDED_SCHEME,https``.
If clients can reach the app without passing through such a proxy, disable the
trust entirely by setting ``DJANGO_SECURE_PROXY_SSL_HEADER`` to an empty
value.

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

Note that this setup writes no log files anywhere: Gunicorn and the scheduled
jobs log to the journal through their systemd units, and so does Caddy's
process log. Caddy's per-request access logging is disabled by default; add a
bare ``log`` directive to the site block if you want it, and it goes to the
journal as well.


Scheduled jobs
==============

To fetch new releases you must run ``get_releases`` regularly, and you should run
``clearsessions`` to purge expired sessions. Run each as a short-lived container
from a systemd user timer. Because the container is stateless, these reuse the
same image, env file, media mount, ``keep-id`` mapping, and pasta port
forwarding as the web service.

Create ``~/.config/systemd/user/comics-get-releases.service``:

.. code-block:: ini

    [Unit]
    Description=Fetch new comics releases

    [Service]
    Type=oneshot
    ExecStart=/usr/bin/podman run --rm \
        --userns=keep-id:uid=1000,gid=1000 \
        --volume=/srv/comics/media:/media:rw \
        --env-file=/srv/comics/comics.env \
        --network=pasta:-T,5432,-T,11211,-T,25 \
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


Management commands
===================

Any other management command can be run the same way as the scheduled jobs: as
a one-off container sharing the same mounts and settings. For example, to
create a superuser::

    podman run --rm -it \
        --userns=keep-id:uid=1000,gid=1000 \
        --volume=/srv/comics/media:/media:rw \
        --env-file=/srv/comics/comics.env \
        --network=pasta:-T,5432,-T,11211,-T,25 \
        ghcr.io/jodal/comics:latest comics createsuperuser

See :doc:`bootstrapping` for the commands to populate a fresh site with comics
and releases.
