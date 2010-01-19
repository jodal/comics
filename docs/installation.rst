************
Installation
************

Software requirements
=====================

Minimum dependencies
--------------------

The absolute minimum requirements for getting *comics* up and running is:

- `Python <http://www.python.org/>`_ >= 2.5
- `PIL <http://www.pythonware.com/products/pil/>`_ >= 1.1
- `Django <http://www.djangoproject.com/>`_ >= 1.1
- `South <http://south.aeracode.org/>`_ >= 0.6
- `feedparser <http://www.feedparser.org/>`_ >= 4.0
- `lxml <http://codespeak.net/lxml/>`_ >= 2.0

To install these on Ubuntu 9.10, run::

    sudo aptitude install python-pip python-django python-feedparser \
        python-lxml python-imaging
    sudo pip install South

To install these on Ubuntu 10.04, run::

    sudo aptitude install python-django python-django-south python-feedparser \
        python-lxml python-imaging

If you are running Mac OS X with `MacPorts <http://www.macports.org/>`_
installed, you can install the dependencies by running::

    sudo ports install python26 py26-django py26-south py26-feedparser \
        py26-lxml py26-pil

If you would like to use `pip <http://pip.openplans.org/>`_ to install these
dependencies, a ``requirements.txt`` file for pip is provided with the
*comics* source code.


Optional dependencies for real deployments
------------------------------------------

Optional dependencies (listed by Debian package names) if you want to use a
real database and/or memcache:

- python-psycopg2
- postgresql-X.Y (postgresql-8.3 has been used for development)
- cmemcache (from source, or alternatively python-memcache)


Optional dependencies for development
-------------------------------------

Additional dependencies which are handy for development:

- python-pmock (for mocking in unit tests)
- python-coverage (for checking test coverage)
- python-sphinx (for generating HTML documentation)
- python-django-debug-toolbar (for debugging)
- python-django-extensions (for generating the data model diagram)


Get *comics*
============

You can get hold of *comics* in two ways:

- Download the lastest release from http://github.com/jodal/comics/downloads.
- Get the latest development version of *comics* by cloning the Git
  repository, by running ``git clone git://github.com/jodal/comics``.


Run *comics*
============

To get *comics* to a state useful for testing of new crawlers and personal
usage, the following steps are all that is needed.


Create database
---------------

A file-based SQLite database will be used, unless you have created a file
``comics/comics/settings/local.py`` where you have configured another database,
like PostgreSQL.

To create the database and database schema, open a terminal, go to the
``comics/comics/`` directory, and run::

    python manage.py syncdb

Parts of the database is managed by the South database migrations tool. To
create that part of the database, run::

    python manage.py migrate


Seed database
-------------

Then we need to seed the database with information on what comics exist::

    python manage.py loadmeta

Optionally, you can add ``-c xkcd`` to only load the *XKCD* comic from
``comics/comics/comics/xkcd.py``.


Get some comics
---------------

Next, we need to get hold of some comic releases, so we will crawl the web for
them::

    python manage.py getcomics


Development web server
----------------------

Finally, to be able to browse the comic releases we have aggregated, start the
Django development web server by running::

    python manage.py runserver

If you now point your web browser at http://localhost:8000/ you will be able to
browse all available comics. If you provided a username and password at the
``syncdb`` step, you can log in at http://localhost:8000/admin/ to do simple
administration tasks, like removing comics or releases.


Final notes
-----------

All of these commands answers to the ``--help`` argument. I.e. ``getcomics``
can crawl specific comics, and arbitrary ranges of dates instead of just
getting the latest release.

