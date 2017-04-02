Installation
************

First of all, *comics* is just a `Django <https://www.djangoproject.com/>`_
application. Thus, if there are details not outlined in *comics*' own docs,
you'll probably find the answer in Django's docs. For example, database
settings are mentioned on this page, but no details are given, as we're just
talking about Django's database settings. Django got better docs for their
database settings than we could ever write, so please refer to Django's docs.


Get *comics*
============

You can get hold of *comics* in two ways:

- Download the lastest release from https://github.com/jodal/comics/tags and
  unpack it.

- Clone the Git repository. You can do so by running::

      git clone https://github.com/jodal/comics.git
      cd comics/

  You'll then find the current stable/maintenance version in the ``master``
  branch::

      git checkout master

  And the current development version in the ``develop`` branch::

      git checkout develop


Software requirements
=====================

It is recommended to create a `virtualenv <https://virtualenv.pypa.io/>`_ to
isolate the dependencies from other applications on the same system::

    cd comics/
    virtualenv ../comics-virtualenv/

Every time you want to use the virtualenv, it must be activated::

    source ../comics-virtualenv/bin/activate

The dependencies can be installed using `pip <https://pip.pypa.io/>`_::

    pip install -r requirements.txt

If you make use of a virtualenv for a real deployment, you'll also need to make
sure that the WSGI file and the cronjob activate the virtualenv.


Minimum dependencies
--------------------

The absolute minimum requirements for getting *comics* up and running are
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


Run *comics*
============

To get *comics* to a state useful for testing of new crawlers and personal
usage, the following steps are all that is needed.


Create database
---------------

A file-based SQLite database will be used, unless you have configured another
database, like PostgreSQL.

To create the database and database schema, open a terminal, go to top level
directory in your checkout of the comics repo, where you'll find the file
``manage.py``, and run::

    python manage.py migrate

When migrate has finished, create a superuser by running::

    python manage.py createsuperuser


Seed database
-------------

Then we need to seed the database with information on what comics to crawl.
E.g. to add the *XKCD* comic from ``comics/comics/comics/xkcd.py``, run::

    python manage.py comics_addcomics -c xkcd

Optionally, you can add all available active comics to the database::

    python manage.py comics_addcomics -c all


Get some comic releases
-----------------------

Next, we need to get hold of some comic releases, so we will crawl the web for
them. This will get today's releases for all added comics::

    python manage.py comics_getreleases

To get the release for a specific added comics, you can filter with
:option:`--comic` or :option:`-c`::

    python manage.py comics_getreleases -c xkcd

To get releases for a range of days, you can specify a date range with
:option:`--from` or :option:`-f` and :option:`--to` or :option:`-t`. Both
defaults to today, so you can leave the end of the range out::

    python manage.py comics_getreleases -f 2011-11-11


Development web server
----------------------

Finally, to be able to browse the comic releases we have aggregated, start the
Django development web server by running::

    python manage.py runserver

If you now point your web browser at http://localhost:8000/ you will be able to
browse all available comics. If you created a superuser above, you can log in
at http://localhost:8000/admin/ to do simple administration tasks, like
removing comics or releases.


More options
------------

All of the ``manage.py`` commands got more options available. Add the
:option:`--help` argument to any of the commands to get a full listing of the
available options.
