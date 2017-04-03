**********
Deployment
**********

The following example documents *one way* to deploy *comics*. As *comics* is a
standard Django project with an additional batch job for crawling, it may be
deployed in just about any way a Django project may be deployed. Please refer
to `Django's deployment documentation
<https://docs.djangoproject.com/en/dev/howto/deployment/>`_ for further
details.

In the following examples we assume that we are deploying *comics* at
http://comics.example.com/, using Apache, mod_wsgi, and PostgreSQL. The Django
application and batch job is both running as the user ``comics-user``. The
static media files, like comic images, are served from
http://comics.example.com/media/, but may also be served from a different host.


Database
========

*comics* should theoretically work with any database supported by Django.
Though, development is mostly done on SQLite and PostgreSQL. For production
use, PostgreSQL is the recommended choice.

.. note::

    If you are going to use SQLite in a deployment with Apache and so on, you
    need to ensure that the user the web server will be running as has write
    access to the *directory* the SQLite database file is located in.

Additional database indexes
---------------------------

Out of the box, *comics* will create a few extra database indexes that will
make it a lot more performant. In addition, creating the following indexes will
improve performance a bit more:

.. code-block:: sql

    CREATE INDEX comics_release_comic_id_pub_date
        ON comics_release (comic_id, pub_date);


Example Apache vhost
====================

This example requires your Apache to have the ``mod_wsgi`` module. For
efficient static media serving and caching, you should probably enable
``mod_deflate`` and ``mod_expires`` for ``/media`` and ``/static``.

.. code-block:: apache

    <VirtualHost *:80>
        ServerName comics.example.com
        ErrorLog /var/log/apache2/comics.example.com-error.log
        CustomLog /var/log/apache2/comics.example.com-access.log combined

        # Not used, but Apache will complain if the dir does not exist
        DocumentRoot /var/www/comics.example.com

        # Static media hosting
        Alias /media/ /path/to/comics/media/
        Alias /static/ /path/to/comics/static/

        # mod_wsgi setup
        WSGIDaemonProcess comics user=comics-user group=comics-user threads=50 maximum-requests=10000
        WSGIProcessGroup comics
        WSGIScriptAlias / /path/to/comics/comics/wsgi.py
        <Directory /path/to/comics/comics>
            Require all granted
        </Directory>
    </VirtualHost>

For details, please refer to the documentation of the `Apache
<http://httpd.apache.org/docs/>`_ and `mod_wsgi
<http://code.google.com/p/modwsgi/>`_ projects.


Example ``.env``
================

To change settings, you should not change the settings files shipped with
*comics*, but instead override the settings in the apps environment or in the
file ``comics/.env``.  Even if you do not want to override any default
settings, you must at least set ``DJANGO_SECRET_KEY`` and most probably your
database settings. A full set of environment variables for a production
deployment may look like this::

    VIRTUALENV_ROOT=/srv/example.com/venv

    DJANGO_SECRET_KEY=Kaikoh9aiye7air9dae5aigh9ue1Ooc7

    DJANGO_ADMIN=comics@example.com
    DJANGO_DEFAULT_FROM_EMAIL=comics@example.com

    DJANGO_MEDIA_ROOT=/var/www/static.example.com/media/
    DJANGO_MEDIA_URL=http://static.example.com/media/
    DJANGO_STATIC_ROOT=/var/www/static.example.com/static/
    DJANGO_STATIC_URL=http://static.example.com/static/

    DATABASE_URL=postgres://comics:topsecret@localhost:5432/comics

    MEMCACHED_URL=127.0.0.1:11211

Of course, you should change most, if not all, of these settings for your own
installation. If your are not running a *memcached* server, remove the part on
caching from your ``local.py``.


.. _collecting-static-files:

Collecting static files
=======================

When you're not running in development mode, you'll need to collect the static
files from all apps into the ``STATIC_ROOT``. To do this, run::

    python manage.py collectstatic

You have to rerun this command every time you deploy changes to graphics, CSS
and JavaScript. For more details, see the Django documentation on `staticfiles
<https://docs.djangoproject.com/en/1.7/howto/static-files/>`_.


Example cronjob
===============

To get new comics, you should run ``comics_getreleases`` regularly. In
addition, you should run ``cleanupinvitation`` once in a while to remove
expired user invitations and ``cleanupregistration`` to delete expired users.
One way is to use ``cron`` e.g. by placing the following in
``/etc/cron.d/comics``:

.. code-block:: sh

    MAILTO=comics@example.com
    PYTHONPATH=/path/to/comics
    1 * * * * comics-user python /path/to/comics/manage.py comics_getreleases -v0
    1 3 * * * comics-user python /path/to/comics/manage.py cleanupinvitation -v0
    2 3 * * * comics-user python /path/to/comics/manage.py cleanupregistration -v0

If you have installed *comics*' dependencies in a virtualenv instead of
globally, the cronjob must also activate the virtualenv. This can be done by
using the ``python`` interpreter from the virtualenv:

.. code-block:: sh

    MAILTO=comics@example.com
    PYTHONPATH=/path/to/comics
    1 * * * * comics-user /path/to/comics-virtualenv/bin/python /path/to/comics/manage.py comics_getreleases -v0
    1 3 * * * comics-user /path/to/comics-virtualenv/bin/python /path/to/comics/manage.py cleanupinvitation -v0
    2 3 * * * comics-user /path/to/comics-virtualenv/bin/python /path/to/comics/manage.py cleanupregistration -v0

By setting ``MAILTO`` any exceptions raised by the comic crawlers will be sent
by mail to the given mail address. ``1 * * * *`` specifies that the command
should be run 1 minute past every hour.
