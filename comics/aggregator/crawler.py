import datetime as dt
import time

from comics.aggregator.exceptions import *
from comics.aggregator.feedparser import FeedParser
from comics.aggregator.lxmlparser import LxmlParser
from comics.core.models import Release, Strip

class CrawlerResult(object):
    def __init__(self, url, title=None, text=None, headers=None):
        self.url = url
        self.title = title
        self.text = text
        self.headers = headers

class CrawlerBase(object):
    # Whether to allow multiple releases per day
    multiple_releases_per_day = False

    # Whether to check the mime type of the strip image when downloading
    check_image_mime_type = True

    # Feed object which is reused when crawling multiple dates
    feed = None

    def __init__(self, comic):
        self.comic = comic

    def get_strip_metadata(self, pub_date=None):
        """Get URL of strip from pub_date, or the latest strip"""

        self.pub_date = self._get_date_to_crawl(pub_date)
        result = self.crawl(self.pub_date)
        if result:
            self._check_strip_url(result)
            if self.feed:
                self._decode_feed_data(result)

            # TODO Make sure additional HTTP headers are transfered to the
            # downloader
            return {
                'comic': self.comic,
                'check_image_mime_type': self.check_image_mime_type,
                'pub_date': pub_date,
                'url': result.url,
                'title': result.title,
                'text': result.text,
            }

    def _get_date_to_crawl(self, pub_date):
        if pub_date is None:
            pub_date = dt.date.today()

        if not self.comic.history_capable() and pub_date != dt.date.today():
            raise NotHistoryCapable

        if (self.comic.history_capable() and
                pub_date < self.comic.history_capable()):
            raise OutsideHistoryCapabilityRange(
                'Not history capable, less than %s' %
                self.comic.history_capable())

        if not self.multiple_releases_per_day:
            if Release.objects.filter(comic=self.comic,
                    pub_date=pub_date).count():
                raise StripAlreadyExists('%s/%s' % (self.comic.slug, pub_date))

        return pub_date

    def _check_strip_url(self, result):
        """Validate strip URL found by the crawler"""

        if not result.url:
            raise StripURLNotFound('%s/%s' % (self.comic.slug, self.pub_date))

    def _decode_feed_data(self, result):
        """Decode titles and text retrieved from a feed"""

        if (self.feed.raw_feed.encoding
                and self.feed.raw_feed.encoding != 'utf-8'):
            if result.title and type(result.title) != unicode:
                result.title = unicode(
                    result.title, self.feed.raw_feed.encoding)
            if result.text and type(result.text) != unicode:
                result.text = unicode(result.text, self.feed.raw_feed.encoding)
        return result

    def crawl(self, pub_date):
        """
        Must be overridden by all crawlers

        Input:
            pub_date -- a datetime.date object for the date to crawl

        Output:
            on success: a CrawlResult object containing:
                - at least a strip image URL
                - optionally a strip title and/or a strip text
            on failure: None
        """

        raise NotImplementedError

    ### Helpers for the crawl() implementations

    def parse_feed(self, feed_url):
        if self.feed is None:
            self.feed = FeedParser(feed_url)
        return self.feed

    def parse_page(self, page_url):
        return LxmlParser(page_url)

    def string_to_date(self, *args, **kwargs):
        return dt.datetime.strptime(*args, **kwargs).date()

    def date_to_epoch(self, date):
        return int(time.mktime(date.timetuple()))


class ComicsComCrawlerBase(CrawlerBase):
    """Base comic crawler for all comics hosted at comics.com"""

    check_image_mime_type = False

    def crawl_helper(self, comics_com_title, pub_date):
        page_url = 'http://comics.com/%(slug)s/%(date)s/' % {
            'slug': comics_com_title.lower().replace(' ', '_'),
            'date': pub_date.strftime('%Y-%m-%d'),
        }
        page = self.parse_page(page_url)
        url = page.src('a.STR_StripImage img[alt^="%s"]' % comics_com_title)
        return CrawlerResult(url)
