Installation
************

First of all, Comics is just a `Django <https://www.djangoproject.com/>`_
application. Thus, if there are details not outlined in Comics' own docs,
you'll probably find the answer in Django's docs. For example, database
settings are mentioned on this page, but no details are given, as we're just
talking about Django's database settings. Django got better docs for their
database settings than we could ever write, so please refer to Django's docs.


Get release
===========

You can get hold of Comics in two ways:

- Download the lastest release from https://github.com/jodal/comics/releases.

- Clone the Git repository. You can do so by running::

      git clone https://github.com/jodal/comics.git

  You'll then have the latest development snapshot in the ``main`` branch::

      cd comics/

  If you want to run a specific release, they are available as tags in the
  Git repository. If you checkout a tag name, you'll have exactly the same as
  you find in the release archives::

      git tag -l
      git checkout v4.0.0


Software requirements
=====================

First of all, you need Python 3.7 or newer.

It is recommended to create a virtualenv to isolate the dependencies from
other applications on the same system::

    cd comics/
    python3 -m venv .venv

Every time you want to use the virtualenv, it must be activated::

    source .venv/bin/activate

If you make use of a virtualenv for a real deployment, you'll also need to make
sure that the app server and the cronjob activate the virtualenv.


Minimum dependencies
--------------------

The absolute minimum requirements for getting Comics up and running can be
installed with::

    python3 -m pip install .


Optional dependencies for real deployments
------------------------------------------

To deploy Comics, you need a WSGI server. There are several options, but we
tend to use Gunicorn. To install it, run::

    python -m pip install ".[server]"

By default, Comics is configured to use an SQLite database. While SQLite is
good enough for local development, we recommend PostgreSQL when running
Comics long-term. To install the extra dependencies required to use
PostgreSQL as the database, run::

    python3 -m pip install ".[pgsql]"

Comics does not require a cache, but responses are significantly faster with
a cache available. To install the dependencies required for to use memcached
as a cache, run::

    python3 -m pip install ".[cache]"

The Comics API is able to respond using JSON, XML, or several other formats.
To install the dependencies required to provide all possible response
formats, run::

    python3 -m pip install ".[api]


Development dependencies
------------------------

If you're setting up Comics for development, you should install `Poetry
<https://python-poetry.org/>`_, and in the Comics git repository, run::

    poetry install

This installs both the minimum dependencies as described above and all extra
dependencies required for development.
