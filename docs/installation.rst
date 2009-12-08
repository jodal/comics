************
Installation
************

Software requirements
=====================

Minimum dependencies
--------------------

The absolute minimum requirements for getting *comics* up and running is:

- `Python <http://www.python.org/>`_ >= 2.5
- `Django <http://www.djangoproject.com/>`_ >= 1.0
- `feedparser <http://www.feedparser.org/>`_
- `lxml <http://codespeak.net/lxml/>`_

To install these on Debian-based Linux distributions, like Ubuntu, simply run::

    sudo aptitude install python-django python-feedparser python-lxml

If you are running Mac OS X with `MacPorts <http://www.macports.org/>`_
installed, you can install the dependencies by running::

    sudo ports install python26 py26-django py26-feedparser py26-lxml


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

Get hold of a fresh version of *comics* by cloning the Git repository::

    git clone git://github.com/jodal/comics


Run *comics*
============

To get *comics* to a state useful for testing of new crawlers and personal
usage, the following steps are all that is needed.

A file-based SQLite database will be used by default [#sqlite]_. To create the
database and database schema, open a terminal, go to the ``comics/comics/``
directory, and run::

    python manage.py syncdb

Then we need to seed the database with information on what comics exist::

    python manage.py loadmeta

Optionally, you can add ``-c xkcd`` to only load the *XKCD* comic from
``comics/comics/comics/xkcd.py``.

Next, we need to get hold of some comic strips, so we will crawl the web for
them::

    python manage.py getcomics

Finally, to be able to browse the comic strips we have aggregated, start the
Django development web server by running::

    python manage.py runserver

If you now point your web browser at http://localhost:8000/ you will be able to
browse all available comics. If you provided a username and password at the
``syncdb`` step, you can log in at http://localhost:8000/admin/ to do simple
administration tasks, like removing comics or strips.

All of these commands answers to the ``--help`` argument. I.e. ``getcomics``
can crawl specific comics, and arbitrary ranges of dates instead of just
getting the latest comic strips.


.. rubric:: Footnotes

.. [#sqlite] Unless you have created a file ``comics/comics/settings/local.py``
    where you have configured another database.

