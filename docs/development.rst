***********
Development
***********


Running tests
=============

*comics* got some tests, but far from full test coverage.

To run unit tests::

    python manage.py test --settings=comics.settings.testing

To run unit tests with statement coverage::

    python manage.py test --settings=comics.settings.coverage


Todo list
=========

A mostly unordered list of things to fix. Patches accepted.


Improvements
------------

``comics.comics.pennyarcade``
    Move web page string decoding to comics.aggregator.lxmlparser.
``comics.aggregator.crawler._decode_feed_data()``
    Move feed string decoding to comics.aggregator.feedparser/lxmlparser.
``comics.aggregator.crawler._get_date_to_crawl()``
    Use comics time zone to crawl the correct current date.
``comics.aggregator.command``
    Use comic week schedule to crawl less often on non-schedule days.
``comics.core.utils.navigation``
    Unit test and refactor.


New features
------------

- Support multiple strips per comic per day, which requires:

  - Change of naming scheme for image files from date to checksum.
  - Support for returning multiple ``CrawlerResult`` from one ``crawl()``.


Change specifications
=====================

.. toctree::
    :glob:

    specs/*
