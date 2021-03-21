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
      git checkout v3.0.0


Software requirements
=====================

It is recommended to create a `virtualenv <https://virtualenv.pypa.io/>`_ to
isolate the dependencies from other applications on the same system::

    cd comics/
    virtualenv .venv/

Every time you want to use the virtualenv, it must be activated::

    source .venv/bin/activate

The dependencies can be installed using `pip <https://pip.pypa.io/>`_::

    pip install -r requirements.txt

If you make use of a virtualenv for a real deployment, you'll also need to make
sure that the WSGI file and the cronjob activate the virtualenv.


Minimum dependencies
--------------------

The absolute minimum requirements for getting Comics up and running are
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
