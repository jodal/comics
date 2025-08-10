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
      git checkout v25.8.0


Software requirements
=====================

The simple way is to install `uv <https://docs.astral.sh/uv/>`_, and while in
the `comics` directory, run::

    uv sync --all-extras --all-groups

This will install the correct Python version if needed, create or activate the
virtualenv, and install dependencies.


Minimum dependencies
--------------------

The absolute minimum requirements for getting Comics up and running can be
installed with::

    uv sync --no-dev


Optional dependencies for real deployments
------------------------------------------

To deploy Comics, you need a WSGI server. There are several options, but we
tend to use Gunicorn. To install it, run::

    uv sync --extra server

By default, Comics is configured to use an SQLite database. While SQLite is
good enough for local development, we recommend PostgreSQL when running
Comics long-term. To install the extra dependencies required to use
PostgreSQL as the database, run::

    uv sync --extra pgsql

Comics does not require a cache, but responses are significantly faster with
a cache available. To install the dependencies required for to use memcached
as a cache, run::

    uv sync --extra cache

The Comics API is able to respond using JSON, XML, or several other formats.
To install the dependencies required to provide all possible response
formats, run::

    uv sync --extra api


Development dependencies
------------------------

If you're setting up Comics for development, you should install `uv
<https://docs.astral.sh/uv/>`_, and in the Comics git repository, run::

    uv sync --all-extras --all-groups

This installs both the minimum dependencies as described above and all extra
dependencies required for development.
