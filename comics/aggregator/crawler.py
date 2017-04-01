import datetime
import httplib
import socket
import time
import urllib2
import xml.sax._exceptions

from django.utils import timezone

import pytz

from comics.aggregator.exceptions import (
    CrawlerHTTPError, ImageURLNotFound, NotHistoryCapable,
    ReleaseAlreadyExists)
from comics.aggregator.feedparser import FeedParser
from comics.aggregator.lxmlparser import LxmlParser

# For testability
now = timezone.now
today = datetime.date.today


class CrawlerRelease(object):
    def __init__(self, comic, pub_date, has_rerun_releases=False):
        self.comic = comic
        self.pub_date = pub_date
        self.has_rerun_releases = has_rerun_releases
        self._images = []

    @property
    def identifier(self):
        return u'%s/%s' % (self.comic.slug, self.pub_date)

    @property
    def images(self):
        return self._images

    def add_image(self, image):
        image.validate(self.identifier)
        self._images.append(image)


class CrawlerImage(object):
    def __init__(self, url, title=None, text=None, headers=None):
        self.url = url
        self.title = title
        self.text = text
        self.request_headers = headers or {}

        # Convert from e.g. lxml.etree._ElementUnicodeResult to unicode
        if self.title is not None and type(self.title) != unicode:
            self.title = unicode(self.title)
        if self.text is not None and type(self.text) != unicode:
            self.text = unicode(self.text)

    def validate(self, identifier):
        if not self.url:
            raise ImageURLNotFound(identifier)


class CrawlerBase(object):
    # ### Crawler settings
    # Date of oldest release available for crawling
    history_capable_date = None
    # Number of days a release is available for crawling
    history_capable_days = None
    # On what weekdays the comic is published (example: "Mo,We,Fr")
    schedule = None
    # In approximately what time zone the comic is published
    # (example: "Europe/Oslo")
    time_zone = 'UTC'
    # Whether to allow multiple releases per day
    multiple_releases_per_day = False

    # ### Downloader settings
    # Whether the comic reruns old images as new releases
    has_rerun_releases = False

    # ### Settings used for both crawling and downloading
    # Dictionary of HTTP headers to send when retrieving items from the site
    headers = {}

    # Feed object which is reused when crawling multiple dates
    feed = None

    # Page objects mapped against URL for use when crawling multiple dates
    pages = {}

    def __init__(self, comic):
        self.comic = comic

    def get_crawler_release(self, pub_date=None):
        """Get meta data for release at pub_date, or the latest release"""

        pub_date = self._get_date_to_crawl(pub_date)
        release = CrawlerRelease(
            self.comic, pub_date, has_rerun_releases=self.has_rerun_releases)

        try:
            results = self.crawl(pub_date)
        except urllib2.HTTPError as error:
            raise CrawlerHTTPError(release.identifier, error.code)
        except urllib2.URLError as error:
            raise CrawlerHTTPError(release.identifier, error.reason)
        except httplib.BadStatusLine:
            raise CrawlerHTTPError(release.identifier, 'BadStatusLine')
        except socket.error as error:
            raise CrawlerHTTPError(release.identifier, error)
        except xml.sax._exceptions.SAXException as error:
            raise CrawlerHTTPError(release.identifier, str(error))

        if not results:
            return

        if not hasattr(results, '__iter__'):
            results = [results]

        for result in results:
            # Use HTTP headers when requesting images
            result.request_headers.update(self.headers)
            release.add_image(result)

        return release

    def _get_date_to_crawl(self, pub_date):
        identifier = u'%s/%s' % (self.comic.slug, pub_date)

        if pub_date is None:
            pub_date = self.current_date

        if pub_date < self.history_capable:
            raise NotHistoryCapable(identifier, self.history_capable)

        if self.multiple_releases_per_day is False:
            if self.comic.release_set.filter(pub_date=pub_date).count() > 0:
                raise ReleaseAlreadyExists(identifier)

        return pub_date

    @property
    def current_date(self):
        tz = pytz.timezone(self.time_zone)
        now_in_tz = tz.normalize(now().astimezone(tz))
        return now_in_tz.date()

    @property
    def history_capable(self):
        if self.history_capable_date is not None:
            return datetime.datetime.strptime(
                self.history_capable_date, '%Y-%m-%d').date()
        elif self.history_capable_days is not None:
            return (today() - datetime.timedelta(self.history_capable_days))
        else:
            return today()

    def crawl(self, pub_date):
        """
        Must be overridden by all crawlers

        Input:
            pub_date -- a datetime.date object for the date to crawl

        Output:
            on success: a CrawlResult object containing:
                - at least an image URL
                - optionally a title and/or a text
            on failure: None
        """

        raise NotImplementedError

    # ### Helpers for the crawl() implementations

    def parse_feed(self, feed_url):
        if self.feed is None:
            self.feed = FeedParser(feed_url)
        return self.feed

    def parse_page(self, page_url):
        if page_url not in self.pages:
            self.pages[page_url] = LxmlParser(page_url, headers=self.headers)
        return self.pages[page_url]

    def string_to_date(self, *args, **kwargs):
        return datetime.datetime.strptime(*args, **kwargs).date()

    def date_to_epoch(self, date):
        """The UNIX time of midnight at ``date`` in the comic's time zone"""
        naive_midnight = datetime.datetime(date.year, date.month, date.day)
        local_midnight = pytz.timezone(self.time_zone).localize(naive_midnight)
        return int(time.mktime(local_midnight.utctimetuple()))


class KingFeaturesCrawlerBase(CrawlerBase):
    """Base comic crawler for King Features comics"""

    def crawl_helper(self, domain, pub_date):
        date = pub_date.strftime('%B-')
        date += pub_date.strftime('%d').lstrip('0')
        date += pub_date.strftime('-%Y')
        page_url = 'http://%s/comics/%s' % (domain, date)
        page = self.parse_page(page_url)
        url = page.src('img[src*="safr.kingfeatures.com"]')
        return CrawlerImage(url)


class GoComicsComCrawlerBase(CrawlerBase):
    """Base comic crawler for all comics hosted at gocomics.com"""

    # It doesn't want us getting comics because of a User-Agent check.
    # Look! I'm a nice, normal Internet Explorer machine!
    headers = {
        'User-Agent': (
            'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; '
            'Trident/4.0; .NET CLR 1.1.4322; .NET CLR 2.0.50727; '
            '.NET CLR 3.0.4506.2152; .NET CLR 3.5.30729'),
    }

    def crawl_helper(self, url_name, pub_date):
        page_url = 'http://www.gocomics.com/%s/%s' % (
            url_name, pub_date.strftime('%Y/%m/%d/'))
        page = self.parse_page(page_url)
        page.remove('.feature_item')
        url = page.src('img.strip')
        return CrawlerImage(url)


class PondusNoCrawlerBase(CrawlerBase):
    """Base comics crawler for all comics posted at pondus.no"""

    time_zone = 'Europe/Oslo'

    def crawl_helper(self, url_id):
        page_url = 'http://www.pondus.no/?section=artikkel&id=%s' % url_id
        page = self.parse_page(page_url)
        url = page.src('.imagegallery img')
        return CrawlerImage(url)


class HeltNormaltCrawlerBase(CrawlerBase):
    """Base comics crawler for all comics posted at heltnormalt.no"""

    headers = {'User-Agent': 'Mozilla/5.0'}
    time_zone = 'Europe/Oslo'

    def crawl_helper(self, short_name, pub_date):
        date_string = pub_date.strftime('%Y/%m/%d')
        page_url = 'http://heltnormalt.no/%s/%s' % (short_name, date_string)
        page = self.parse_page(page_url)
        url = page.src('img[src*="/img/%s/%s"]' % (short_name, date_string))
        return CrawlerImage(url)
