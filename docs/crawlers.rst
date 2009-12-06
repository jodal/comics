*********************
Creating new crawlers
*********************

For each comic *comics* is aggregating, we need to create a crawler. At the
time of writing, about 100 crawlers are available in the
``comics/comics/comics/`` directory. They serve as a great source for learning
how to write new crawlers for *comics*.


A crawler example
=================

The crawlers are split in two separate pieces. The ``Meta`` part contains meta
data about the comic used for display at the web site. The ``Crawler`` part
contains properties needed for crawling and the crawler implementation itself.

.. code-block:: python

    from comics.aggregator.crawler import CrawlerBase, CrawlerResult
    from comics.meta.base import MetaBase

    class Meta(MetaBase):
        name = 'xkcd'
        language = 'en'
        url = 'http://www.xkcd.com/'
        start_date = '2005-05-29'
        rights = 'Randall Munroe, CC BY-NC 2.5'

    class Crawler(CrawlerBase):
        history_capable_days = 10
        schedule = 'Mo,We,Fr'
        time_zone = -5

        def crawl(self, pub_date):
            feed = self.parse_feed('http://www.xkcd.com/rss.xml')
            for entry in feed.for_date(pub_date):
                url = entry.summary.src('img[src*="/comics/"]')
                title = entry.title
                text = entry.summary.alt('img[src*="/comics/"]')
                return CrawlerResult(url, title, text)


The ``Meta`` class fields
=========================

``Meta.name``
    *Required.* A string with the name of the comic.

``Meta.language``
    *Required.* A two-letter string with the language code for the language
    used in the comic. Typically ``'en'`` or ``'no'``.

    Code must also be present in ``comics.core.models.Comic.LANGUAGES``.

``Meta.url``
    *Required.* A string with the URL of the comic's web page.

``Meta.start_date``
    *Optional.* The first date the comic was published at.

``Meta.end_date``
    *Optional.* The last date the comic was published at if it is discontinued.

``Meta.rights``
    *Optional.* Name of the author and the comic's license if available.


The ``Crawler`` class fields
============================

Fields used for crawling
------------------------

``Crawler.history_capable_date``
    *Optional.* Date of oldest release available for crawling. Provide this
    *or* ``Crawler.history_capable_days``. If both are present, this one will
    have precedence.

    Example: ``'2008-03-08'``.

``Crawler.history_capable_days``
    *Optional.* Number of days a release is available for crawling. Provide
    this *or* ``Crawler.history_capable_date``.

    Example: ``32``.

``Crawler.schedule``
    *Optional.* On what weekdays the comic is published.

    Example: ``'Mo,We,Fr'`` or ``'Mo,Tu,We,Th,Fr,Sa,Su'``.

``Crawler.time_zone``
    *Optional.* In approximately what time zone (in whole hours relative to
    UTC, without regard to DST) the comic is published.

    Example: ``1`` for central Europe or ``-5`` for eastern U.S.

``Crawler.multiple_releases_per_day``
    *Optional.* Default: ``False``. Whether to allow multiple strip releases
    per a day.

    Example: ``True`` or ``False``.

Fields used for downloading
---------------------------

``Crawler.has_rerun_releases``
    *Optional.* Default: ``False``. Whether the comic reruns old strips as new
    releases.

    Example: ``True`` or ``False``.

``Crawler.check_image_mime_type``
    *Optional.* Default: ``True``. Whether to check the mime type of the strip
    image when downloading.

    Example: ``True`` or ``False``.


The ``Crawler.crawl()`` method
==============================

The ``crawl()`` is where the real work is going on. To start with an example,
let's look at *XKCD*'s ``crawl()`` method::

    def crawl(self, pub_date):
        feed = self.parse_feed('http://www.xkcd.com/rss.xml')
        for entry in feed.for_date(pub_date):
            url = entry.summary.src('img[src*="/comics/"]')
            title = entry.title
            text = entry.summary.alt('img[src*="/comics/"]')
            return CrawlerResult(url, title, text)


Arguments and return values
---------------------------

The ``crawl()`` method takes a single argument, ``pub_date``, which is a
``datetime.date`` object for the date the crawler is currently crawling. The
goal of the method is to return a ``CrawlerResult`` object containing at least
the URL of the strip image for ``pub_date`` and optionally a ``title`` and
``text`` accompanying the image. ``CrawlerResult``'s signature is::

    CrawlerResult(url, title=None, text=None)

This means that you must always supply an URL, and that you can supply a
``text`` without a ``title``. The following are all valid ways to create a
``CrawlerResult``::

    CrawlerResult(url)
    CrawlerResult(url, title)
    CrawlerResult(url, title, text)
    CrawlerResult(url, title=title)
    CrawlerResult(url, text=text)
    CrawlerResult(url, title=title, text=text)

For some crawlers, this is all you need. If the strip image URL is predictable
and based upon the ``pub_date`` in some way, just create the URL with the help
of `Python's strftime documentation
<http://docs.python.org/library/datetime.html#strftime-behavior>`_, and return
it wrapped in a ``CrawlerResult``::

    def crawl(self, pub_date):
        url = 'http://www.example.com/comics/%s.png' % (
            pub_date.strftime('%Y-%m-%d'),)
        return CrawlerResult(url)

Though, for most crawlers, some interaction with RSS or Atom feeds or web pages
are needed. For this a web parser and a feed parser are provided.


The web parser
==============

The web parser, internally known as ``LxmlParser``, uses CSS selectors to
extract content from HTML::

    def crawl(self, pub_date):
        page_url = 'http://ars.userfriendly.org/cartoons/?id=%s' % (
            pub_date.strftime('%Y%m%d'),)
        page = self.parse_page(page_url)
        url = page.src('img[alt^="Strip for"]')
        return CrawlerResult(url)

This is a common pattern for crawlers. Another common patterns is to use a feed
to find the web page URL for the given date, then parse that web page to find
the strip image URL.

For a primer on CSS selectors, see :ref:`css-selectors`.


Available methods
-----------------

``text(selector, default=None)``
    Returns the text contained by the element matching ``selector``.

``src(selector, default=None)``
    Returns the ``src`` attribute of the element matching ``selector``.

    The web parser automatically expands relative URLs in the source, like
    ``/comics/2008-04-13.png`` to a full URL like
    ``http://www.example.com/2008-04-13.png``, so you do not need to think
    about that.

``alt(selector, default=None)``
    Returns the ``alt`` attribute of the element matching ``selector``.

``title(selector, default=None)``
    Returns the ``title`` attribute of the element matching ``selector``.

``remove(selector)``
    Remove the elements matching ``selector`` from the parsed document.

``select(selector)``
    Return the ``lxml`` elements for the elements matching ``selector``.


The feed parser
===============

The feed parser is initialized with a feed URL, just like the web parser is
initialized with a web page URL::

    feed = self.parse_feed('http://www.xkcd.com/rss.xml')


Feed methods
------------

The ``feed`` object provides two methods which both returns feed elements:

``for_date(date)``
    Returns all feed elements published at ``date``.

``all()``
    Returns all feed elements.

Typically, a crawler uses ``for_date(date)`` and loops over all entries it
returns to find the strip image URL::

    for entry in feed.for_date(pub_date):
        # parsing comes here
        return CrawlerResult(url)


Entry fields with ``LxmlParser``
--------------------------------

The *comics* feed parser is really a combination of *`feedparser
<http://www.feedparser.org/>`_* and ``LxmlParser``. It can do anything
*feedparser* can do, and in addition you can use the ``LxmlParser`` methods on
feed fields which contains HTML:

``summary``
    This is the most frequently used entry field which supports HTML parsing
    with the ``LxmlParser`` methods.

``content0``
    This is the same as *feedparser*'s ``content[0].value`` field, but with
    ``LxmlParser`` methods available. For some crawlers, this is where the
    interesting stuff is found.

::

    url = entry.summary.src('img')
    title = entry.summary.alt('img')

If you need to parse HTML in any other fields than the above two, you can apply
the ``html(string)`` method on the field, like it is applied on a feed entry's
title field here::

    title = entry.html(entry.title).text('h1')


.. _css-selectors:

Matching HTML elements using CSS selectors
==========================================

Both web page and feed parsing uses CSS selectors to extract the interesting
strings from HTML. CSS selectors are those normally simple strings you use in
CSS style sheets to select what elements of your web page the CSS declarations
should be applied to.

In the following example ``h1 a`` is the selector. It matches all ``a``
elements contained in ``h1`` elements. The rule to be applied to the matching
elements is ``color: red;``.

.. code-block:: css

    h1 a { color: red; }

Similarly ``class="foo"`` and ``id="bar"`` in HTML may be used in CSS
selectors. The following CSS example would color all ``h1`` headers with the
class ``foo`` red, and all elements with the ID ``bar`` which is contained in
``h1`` elements would be colored blue.

.. code-block:: css

    h1.foo { color red; }
    h1 #bar { color: blue; }

In CSS3, the power of CSS selectors have been greatly increased by the addition
of matching by the content of elements' arguments. To match all ``img``
elements with a ``src`` attribute *starting with* ``http://www.example.com/``
simply write::

    img[src^="http://www.example.com/"]

Or, to match all ``img`` elements whose ``src`` attribute *ends in* ``.jpg``::

    img[src$=".jpg"]

Or, ``img`` elements whose ``src`` attribute *contains* ``/comics/``::

    img[src*="/comics/"]

Or, ``img`` elements whose ``alt`` attribute *is* ``Today's comic``::

    img[alt="Today's comic"]



For further details on CSS selectors in general, please refer to
http://css.maxdesign.com.au/selectutorial/.


Testing your new crawler
========================

**TODO**


Loading ``Meta`` for your new comic
-----------------------------------

**TODO**

::

    python manage.py loadmeta -c newcomic


Running the crawler
-------------------

**TODO**

::

    python manage.py getcomics -c newcomic
