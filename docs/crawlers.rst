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

**TODO**


The web and feed parsers
------------------------

**TODO**


Extracting data from HTML using CSS selectors
---------------------------------------------

**TODO**

**References:**

- http://css.maxdesign.com.au/selectutorial/


