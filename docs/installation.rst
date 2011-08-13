
Installation
************

Software requirements
=====================

The dependencies can be installed using `pip <http://www.pip-installer.org>`_.

You can either install the dependencies globally on your computer::

    cd comics/
    sudo pip install -r requirements.txt

Or, in an isolated environment using `virtualenv
<http://www.virtualenv.org>`_::

    cd comics/
    virtualenv venv/
    source venv/bin/activate
    pip install -r requirements.txt

If you make use of a virtualenv for a real deployment, you'll also need to make
sure that the WSGI file and the cronjob activate the virtualenv.


Minimum dependencies
--------------------

The absolute minimum requirements for getting *comics* up and running is
documented in the file ``requirements.txt``:

.. literalinclude:: ../requirements.txt


Optional dependencies for real deployments
------------------------------------------

For a real deployment, you should consider using another database than SQLite,
which is the default.  In that case, you also need to install Python libraries
for connecting to your database of choice, e.g. ``psycopg2`` if you are using
PostgreSQL.


Optional dependencies for development
-------------------------------------

There are also some additional requirements only needed for development, which
are listed in the file ``requirements-dev.txt``:

.. literalinclude:: ../requirements-dev.txt


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


More options
------------

All of these commands got more options available. I.e. ``getcomics`` can crawl
specific comics, and arbitrary ranges of dates instead of just getting the
latest release. Add the ``--help`` argument to any of the commands to get a
full listing.
