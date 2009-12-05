Installation
============

Dependencies
------------

The dependencies are listed as Debian/Ubuntu package names.

- python (>=2.5)
- python-django (>=1.0)
- python-feedparser
- python-lxml

Optional dependencies if you want to use a real database and/or memcache:

- python-psycopg2
- postgresql-X.Y (developed with 8.3)
- cmemcache (from source, or alternatively python-memcache)

Additional dependencies which are handy for development:

- python-pmock (for mocking in unit tests)
- python-coverage (for checking test coverage)
- debug_toolbar (for debugging, from
  http://code.google.com/p/django-debug-toolbar/)


Installation
------------

To get comics up and running from a clean checkout is as easy as::

    git clone git://github.com/jodal/comics.git
    cd comics/comics/
    python manage.py syncdb
    python manage.py loadmeta
    python manage.py getcomics
    python manage.py runserver

Then point your browser to http://localhost:8000/ to start reading comics.
