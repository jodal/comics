import datetime
import httplib
import socket
import time
import urllib2
import xml.sax._exceptions

from django.conf import settings
from django.utils import timezone

from comics.aggregator.exceptions import (CrawlerHTTPError, ImageURLNotFound,
    NotHistoryCapable, ReleaseAlreadyExists)
from comics.aggregator.feedparser import FeedParser
from comics.aggregator.lxmlparser import LxmlParser

# For testability
now = timezone.now
today = datetime.date.today
utc_offset_in_s = time.timezone


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
    ### Crawler settings
    # Date of oldest release available for crawling
    history_capable_date = None
    # Number of days a release is available for crawling
    history_capable_days = None
    # On what weekdays the comic is published (example: "Mo,We,Fr")
    schedule = None
    # In approximately what time zone (in whole hours relative to UTC, without
    # regard to DST) the comic is published
    time_zone = None
    # Whether to allow multiple releases per day
    multiple_releases_per_day = False

    ### Downloader settings
    # Whether the comic reruns old images as new releases
    has_rerun_releases = False

    ### Settings used for both crawling and downloading
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
        release = CrawlerRelease(self.comic, pub_date,
            has_rerun_releases=self.has_rerun_releases)

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
            raise CrawlerHTTPError(release.identifier, error.message)

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
        if self.time_zone is None:
            self.time_zone = settings.COMICS_DEFAULT_TIME_ZONE
        local_time_zone = - utc_offset_in_s // 3600
        hour_diff = local_time_zone - self.time_zone
        current_time = now() - datetime.timedelta(hours=hour_diff)
        return current_time.date()

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

    ### Helpers for the crawl() implementations

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
        return int(time.mktime(date.timetuple()))


class GoComicsComCrawlerBase(CrawlerBase):
    """Base comic crawler for all comics hosted at gocomics.com"""

    # It doesn't want us getting comics because of a User-Agent check.
    # Look! I'm a nice, normal Internet Explorer machine!
    headers = {
        'User-Agent': 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; '
            'Trident/4.0; .NET CLR 1.1.4322; .NET CLR 2.0.50727; '
            '.NET CLR 3.0.4506.2152; .NET CLR 3.5.30729',
    }

    def crawl_helper(self, short_name, pub_date, url_name=None):
        if url_name is None:
            url_name = short_name
        page_url = 'http://www.gocomics.com/%s/%s' % (
            url_name.lower().replace(' ', ''), pub_date.strftime('%Y/%m/%d/'))
        page = self.parse_page(page_url)
        url = page.src('img.strip[alt="%s"]' % short_name)
        return CrawlerImage(url)


class PondusNoCrawlerBase(CrawlerBase):
    """Base comics crawling for all comics posted at pondus.no"""
    time_zone = 1

    def crawl_helper(self, url_id):
        page_url = 'http://www.pondus.no/?section=artikkel&id=%s' % url_id
        page = self.parse_page(page_url)
        url = page.src('.imagegallery img')
        return CrawlerImage(url)
