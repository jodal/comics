Bootstrapping
=============

Once you've installed Comics, you need to create the database and create the
initial users and comics.

To get Comics to a state useful for testing of new crawlers and personal
usage, the following steps are all that is needed.


Create database
---------------

A file-based SQLite database will be used, unless you have configured another
database, like PostgreSQL.

To create the database and database schema, open a terminal, go to top level
directory in your checkout of the Comics repo, where you'll find the file
``manage.py``, and run::

    python manage.py migrate


Create first user
-----------------

When ``migrate`` has finished, create a superuser by running::

    python manage.py createsuperuser


Add comics
----------

Then we need to seed the database with information on what comics to crawl.
E.g. to add the *XKCD* comic from ``comics/comics/xkcd.py``, run::

    python manage.py comics_addcomics -c xkcd

Optionally, you can add all available active comics to the database::

    python manage.py comics_addcomics -c all


Get comic releases
------------------

Next, we need to get hold of some comic releases, so we will crawl the web for
them. This will get today's releases for all added comics::

    python manage.py comics_getreleases

To get the release for a specific added comics, you can filter with
``--comic`` or ``-c``::

    python manage.py comics_getreleases -c xkcd

To get releases for a range of days, you can specify a date range with
``--from`` or ``-f`` and ``--to`` or ``-t``. Both
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
``--help`` argument to any of the commands to get a full listing of the
available options.
