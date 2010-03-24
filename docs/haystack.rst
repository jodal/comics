******
Search
******

To enable search in Comics you need to install ``django-haystack`` and
setup one of their support `search backends
<http://docs.haystacksearch.org/1.0/installing_search_engines.html>`_.
Consult the `haystack documentation <http://docs.haystacksearch.org/1.0>`_
for information about further settings.

Furthermore ``INSTALLED_APPS`` needs to contain ``haystack`` and ``comics.search``.

Solr
====

Solr needs to be setup with at ``schema.xml`` that knows about the Comics
image model. This file can be created by running ``./manage.py build_solr_schema``.

``./manage.py update_index`` can be run for initial indexing. Subsequent indexing
should be done from cron with for instance ``./manage.py update_index --age=HOURS``,
where ``HOURS`` should be replaced according with how often you reindex.
