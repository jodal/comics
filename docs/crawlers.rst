*********************
Creating new crawlers
*********************

For each comic *comics* is aggregating, we need to create a crawler. At the
time of writing, about 100 crawlers are available in the
``comics/comics/comics/`` directory. They serve as a great source for learning
how to write new crawlers for *comics*.


A crawler example
=================

The crawlers are split in two separate pieces. The :class:`ComicData` part
contains meta data about the comic used for display at the web site. The
:class:`Crawler` part contains properties needed for crawling and the crawler
implementation itself.

::

    from comics.aggregator.crawler import CrawlerBase, CrawlerImage
    from comics.core.comic_data import ComicDataBase

    class ComicData(ComicDataBase):
        name = 'xkcd'
        language = 'en'
        url = 'http://www.xkcd.com/'
        start_date = '2005-05-29'
        rights = 'Randall Munroe, CC BY-NC 2.5'

    class Crawler(CrawlerBase):
        history_capable_days = 10
        schedule = 'Mo,We,Fr'
        time_zone = 'US/Eastern'

        def crawl(self, pub_date):
            feed = self.parse_feed('http://www.xkcd.com/rss.xml')
            for entry in feed.for_date(pub_date):
                url = entry.summary.src('img[src*="/comics/"]')
                title = entry.title
                text = entry.summary.alt('img[src*="/comics/"]')
                return CrawlerImage(url, title, text)


The :class:`ComicData` class fields
===================================

.. class:: ComicData

    .. attribute:: name

        *Required.* A string with the name of the comic.

    .. attribute: language

        *Required.* A two-letter string with the language code for the language
        used in the comic. Typically ``'en'`` or ``'no'``.

        The language code must also be present in
        :attribute:``comics.core.models.Comic.LANGUAGES``.

    .. attribute:: url

        *Required.* A string with the URL of the comic's web page.

    .. attribute:: active

        *Optional.* Wheter or not this comic is still being crawled. Defaults
        to :class:`True`.

    .. attribute:: start_date

        *Optional.* The first date the comic was published at.

    .. attribute:: end_date

        *Optional.* The last date the comic was published at if it is
        discontinued.

    .. attribute:: rights

        *Optional.* Name of the author and the comic's license if available.


The :class:`Crawler` class fields
=================================

.. class:: Crawler

    .. attribute:: history_capable_date

        *Optional.* Date of oldest release available for crawling.

        Provide this *or* :attr:`Crawler.history_capable_days`. If both are
        present, this one will have precedence.

        Example: ``'2008-03-08'``.

    .. attribute:: history_capable_days

        *Optional.* Number of days a release is available for crawling.

        Provide this *or* :attr:`Crawler.history_capable_date`.

        Example: ``32``.

    .. attribute:: schedule

        *Optional.* On what weekdays the comic is published.

        Example: ``'Mo,We,Fr'`` or ``'Mo,Tu,We,Th,Fr,Sa,Su'``.

    .. attribute:: time_zone

        *Optional.* In approximately what time zone the comic is published.

        Example: ``Europe/Oslo`` or ``US/Eastern``.

        See `the IANA timezone database
        <http://en.wikipedia.org/wiki/List_of_tz_database_time_zones>`_ for a
        list of possible values.

    .. attribute:: multiple_releases_per_day

        *Optional.* Default: ``False``. Whether to allow multiple releases per
        day.

        Example: :class:`True` or :class:`False`.

    .. attribute:: has_rerun_releases

        *Optional.* Default: :class:`False`. Whether the comic reruns old
        images as new releases.

        Example: :class:`True`` or :class:`False``.

    .. attribute:: headers

        *Optional.* Default: ``None``. Any HTTP headers to send with any URI
        request for values.

        Useful if you're pulling comics from a site that checks either the
        ``Referer`` or ``User-Agent``. If you can view the comic using your
        browser but not when using your loader for identical URLs, try setting
        the ``Referer`` to be ``http://www.example.com/`` or set the
        ``User-Agent`` to be ``Mozilla/4.0 (compatible; MSIE 8.0; Windows NT
        5.1; Trident/4.0)``.

        Example: ``{'Referer': 'http://www.example.com/', 'Host':
        'http://www.example.com/'}``


The :meth:`Crawler.crawl` method
================================

The :meth:`Crawler.crawl()` is where the real work is going on. To start with
an example, let's look at *XKCD*'s :meth:`Crawler.crawl()` method::

    def crawl(self, pub_date):
        feed = self.parse_feed('http://www.xkcd.com/rss.xml')
        for entry in feed.for_date(pub_date):
            url = entry.summary.src('img[src*="/comics/"]')
            title = entry.title
            text = entry.summary.alt('img[src*="/comics/"]')
            return CrawlerImage(url, title, text)


Arguments and return values
---------------------------

The :meth:`Crawler.crawl()` method takes a single argument, ``pub_date``, which
is a :class:`datetime.date` object for the date the crawler is currently
crawling.  The goal of the method is to return a :class:`CrawlerImage` object
containing at least the URL of the image for ``pub_date`` and optionally a
``title`` and ``text`` accompanying the image. :class:`CrawlerImage`'s
signature is::

    CrawlerImage(url, title=None, text=None)

This means that you must always supply an URL, and that you can supply a
``text`` without a ``title``. The following are all valid ways to create a
``CrawlerImage``::

    CrawlerImage(url)
    CrawlerImage(url, title)
    CrawlerImage(url, title, text)
    CrawlerImage(url, text=text)

For some crawlers, this is all you need. If the image URL is predictable and
based upon the ``pub_date`` in some way, just create the URL with the help
of `Python's strftime documentation
<http://docs.python.org/library/datetime.html#strftime-behavior>`_, and return
it wrapped in a :class:`CrawlerImage`::

    def crawl(self, pub_date):
        url = 'http://www.example.com/comics/%s.png' % (
            pub_date.strftime('%Y-%m-%d'),)
        return CrawlerImage(url)

Though, for most crawlers, some interaction with RSS or Atom feeds or web pages
are needed. For this a :ref:`web parser <web-parser>` and a :ref:`feed parser
<feed-parser>` are provided.


Returning multiple images for a single comic release
----------------------------------------------------

Some comics got releases with multiple images, and thus returning a single
:class:`CrawlerImage` will not be enough for you. For situations like these,
*comics* lets you return a list of :class:`CrawlerImage` objects from
:meth:`Crawler.crawl()`. The list should be ordered in the same way as the
comic is meant to be read, with the first frame as the first element in the
list. If the comic release got a ``title``, add it to the first
:class:`CrawlerImage` object, and let the ``title`` field stay empty on the
rest of the list elements. The same applies for the ``text`` field, unless each
image actually got a different ``title`` or ``text`` string.

The following is an example of a :meth:`Crawler.crawl()` method which returns
multiple images. It adds a ``title`` to the first list element, and different
``text`` to all of the elements.

::

    def crawl(self, pub_date):
        feed = self.parse_feed('http://feeds.feedburner.com/Pidjin')
        for entry in feed.for_date(pub_date):
            result = []
            for i in range(1, 10):
                url = entry.content0.src('img[src$="000%d.jpg"]' % i)
                text = entry.content0.title('img[src$="000%d.jpg"]' % i)
                if url and text:
                    result.append(CrawlerImage(url, text=text))
            if result:
                result[0].title = entry.title
            return result


.. _web-parser:
.. module:: comics.aggregator.lxmlparser

:class:`LxmlParser` -- Parsing web pages and HTML
=================================================

The web parser, internally known as :class:`LxmlParser`, uses CSS selectors to
extract content from HTML. For a primer on CSS selectors, see
:ref:`css-selectors`.

The web parser is accessed through the :meth:`Crawler.parse_page` method::

    def crawl(self, pub_date):
        page_url = 'http://ars.userfriendly.org/cartoons/?id=%s' % (
            pub_date.strftime('%Y%m%d'),)
        page = self.parse_page(page_url)
        url = page.src('img[alt^="Strip for"]')
        return CrawlerImage(url)

This is a common pattern for crawlers. Another common patterns is to use a feed
to find the web page URL for the given date, then parse that web page to find
the image URL.



:class:`LxmlParser` API
-----------------------

The available methods only require a CSS selector, ``selector``, to match tags.
In the event that the selector doesn't match any elements, ``default`` will be
returned.

If the ``selector`` matches multiple elements, one of two things will happen:

- If ``allow_multiple`` is :class:`False`, a :class:`MultipleElementsReturned`
  exception is raised.
- If ``allow_multiple`` is :class:`True`, a list of zero or more elements is
  returned with all of the elements matching ``selector``.

.. class:: LxmlParser

    .. method:: text(selector[, default=None, allow_multiple=False])

        Returns the text contained by the element matching ``selector``.

    .. method:: src(selector[, default=None, allow_multiple=False])

        Returns the ``src`` attribute of the element matching ``selector``.

        The web parser automatically expands relative URLs in the source, like
        ``/comics/2008-04-13.png`` to a full URL like
        ``http://www.example.com/2008-04-13.png``, so you do not need to think
        about that.

    .. method:: alt(selector[, default=None, allow_multiple=False])

        Returns the ``alt`` attribute of the element matching ``selector``.

    .. method:: title(selector[, default=None, allow_multiple=False])

        Returns the ``title`` attribute of the element matching ``selector``.

    .. method:: href(selector[, default=None, allow_multiple=False])

        Returns the ``href`` attribute of the element matching ``selector``.

    .. method:: value(selector[, default=None, allow_multiple=False])

        Returns the ``value`` attribute of the element matching ``selector``.

    .. method:: id(selector[, default=None, allow_multiple=False])

        Returns the ``id`` attribute of the element matching ``selector``.

    .. method:: remove(selector)

        Remove the elements matching ``selector`` from the parsed document.


.. _css-selectors:

Matching HTML elements using CSS selectors
------------------------------------------

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
of matching by the content of elements' attributes. To match all ``img``
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


.. _feed-parser:
.. module:: comics.aggregator.feedparser

:class:`FeedParser` -- Parsing feeds
====================================

The feed parser is initialized with a feed URL passed to
:meth:`Crawler.parse_feed`, just like the web parser is initialized with a web
page URL::

    def crawl(pub_date):
        ...
        feed = self.parse_feed('http://www.xkcd.com/rss.xml')
        ...


:class:`FeedParser` API
-----------------------

The ``feed`` object provides two methods which both returns feed elements:
:meth:`FeedParser.for_date` and :meth:`FeedParser.all`. Typically, a crawler
uses :meth:`FeedParser.for_date` and loops over all entries it returns to find
the image URL::

    for entry in feed.for_date(pub_date):
        # parsing comes here
        return CrawlerImage(url)

.. class:: FeedParser

    .. method:: for_date(date)

        Returns all feed elements published at ``date``.

    .. method:: all()

        Returns all feed elements.


Feed :class:`Entry` API
-----------------------

The *comics* feed parser is really a combination of the popular `feedparser
<http://www.feedparser.org/>`_ library and :class:`LxmlParser
<comics.aggregator.lxmlparser.LxmlParser>`. It can do anything *feedparser* can
do, and in addition you can use the :class:`LxmlParser
<comics.aggregator.lxmlparser.LxmlParser>` methods on feed fields which
contains HTML, like :attr:`Entry.summary` and :attr:`Entry.content0`.

.. class:: Entry

    .. attribute:: summary

        This is the most frequently used entry field which supports HTML
        parsing with the :class:`LxmlParser
        <comics.aggregator.lxmlparser.LxmlParser>` methods.

        Example usage::

            url = entry.summary.src('img')
            title = entry.summary.alt('img')

    .. attribute:: content0

        This is the same as *feedparser*'s ``content[0].value`` field, but with
        :class:`LxmlParser <comics.aggregator.lxmlparser.LxmlParser>` methods
        available. For some crawlers, this is where the interesting stuff is
        found.

    .. method:: html(string)

        Wrap ``string`` in a :class:`LxmlParser
        <comics.aggregator.lxmlparser.LxmlParser>`.

        If you need to parse HTML in any other fields than :attr:`summary` and
        :attr:`content0`, you can apply the ``html(string)`` method on the
        field, like it is applied on a feed entry's title field here::

            title = entry.html(entry.title).text('h1')

    .. attribute:: tags

        List of tags associated with the entry.


Testing your new crawler
========================

When the first version of you crawler is complete, it's time to test it.

The file name is important, as it is used as the comic's slug. This means that
it must be unique within the *comics* installation, and that it is used in the
URLs *comics* will serve the comic at. For this example, we call the crawler
file ``foo.py``. The file must be placed in the ``comics/comics/comics/``
directory, and will be available in Python as ``comics.comics.foo``.


Loading :class:`ComicData` for your new comic
---------------------------------------------

For *comics* to know about your new crawler, you need to load the comic meta
data into *comics*'s database. To do so, we run the ``comics_addcomics``
command::

    python manage.py comics_addcomics -c foo

If you do any changes to the :class:`ComicData` class of any crawler, you must
rerun ``comics_addcomics`` to update the database representation of the comic.


Running the crawler
-------------------

When ``comics_addcomics`` has created a :class:`comics.core.models.Comic`
instance for the new crawler, you may use your new crawler to fetch the comic's
release for the current date by running::

    python manage.py comics_getreleases -c foo

If you want to get comics releases for more than the current day, you may
specify a date range to crawl, like::

    python manage.py comics_getreleases -c foo -f 2009-01-01 -t 2009-03-31

The date range will automatically be adjusted to the crawlers *history
capability*. You may also get comics for a date range without a specific end.
In which case, the current date will be used instead::

    python manage.py comics_getreleases -c foo -f 2009-01-01

If your new crawler is not working properly, you may add ``-v2`` to the command
to turn on full debug output::

    python manage.py comics_getreleases -c foo -v2

For a full overview of ``comics_getreleases`` options, run::

    python manage.py comics_getreleases --help


Submitting your new crawler for inclusion in *comics*
=====================================================

When your crawler is working properly, you may submit it for inclusion in
*comics*. You should fork *comics* at `GitHub
<http://github.com/jodal/comics>`_, commit your new crawler to your own fork,
and send me a *pull request* through GitHub.

All contributions must be granted under the same license as *comics* itself.
