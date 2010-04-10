******
Search
******

To enable search in *comics* you need to install ``django-haystack`` and
setup one of their support `search backends
<http://docs.haystacksearch.org/1.0/installing_search_engines.html>`_.
Consult the `Haystack documentation <http://docs.haystacksearch.org/1.0>`_
for information about further settings.

Furthermore ``INSTALLED_APPS`` needs to contain ``haystack`` and
``comics.search``. E.g. in your ``comics/settings/local.py``, add::

    from comics.settings.base import INSTALLED_APPS
    INSTALLED_APPS += ('haystack', 'comics.search')


Solr schema
===========

Solr needs to be setup with at ``schema.xml`` that knows about the Comics
image model. This file can be created by running::

    python manage.py build_solr_schema


Indexing
========

For initial indexing, run::

    python manage.py update_index

Subsequent indexing should be done from ``cron`` with for instance::

    python manage.py update_index --age=HOURS

where ``HOURS`` should be replaced according with how often you reindex.
