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
        self.request_headers = headers or {}

    def validate(self, comic, pub_date):
        self.comic = comic
        self.pub_date = pub_date
        self._check_strip_url()

    def set_download_settings(self, check_image_mime_type, has_rerun_releases):
        self.check_image_mime_type = check_image_mime_type
        self.has_rerun_releases = has_rerun_releases

    def _check_strip_url(self):
        if not self.url:
            raise StripURLNotFound(self.identifier)

    @property
    def identifier(self):
       return u'%s/%s' % (self.comic.slug, self.pub_date)

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
    # Whether the comic reruns old strips as new releases
    has_rerun_releases = False
    # Whether to check the mime type of the strip image when downloading
    check_image_mime_type = True

    # Feed object which is reused when crawling multiple dates
    feed = None

    def __init__(self, comic):
        self.comic = comic

    def get_strip_metadata(self, pub_date=None):
        """Get URL of strip from pub_date, or the latest strip"""

        pub_date = self._get_date_to_crawl(pub_date)
        result = self.crawl(pub_date)
        if result is not None:
            result.validate(self.comic, pub_date)
            result.set_download_settings(
                check_image_mime_type=self.check_image_mime_type,
                has_rerun_releases=self.has_rerun_releases)
            if self.feed:
                result = self._decode_feed_data(result)
            return result

    def _get_date_to_crawl(self, pub_date):
        if pub_date is None:
            pub_date = dt.date.today()

        if pub_date < self.history_capable():
            raise NotHistoryCapable(self.history_capable())

        if not self.multiple_releases_per_day:
            if Release.objects.filter(comic=self.comic,
                    pub_date=pub_date).count():
                raise StripAlreadyExists('%s/%s' % (self.comic.slug, pub_date))

        return pub_date

    def history_capable(self):
        if self.history_capable_date is not None:
            return self.history_capable_date
        elif self.history_capable_days is not None:
            return (dt.date.today() - dt.timedelta(self.history_capable_days))
        else:
            return dt.date.today()

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

    def schedule_as_isoweekday(self):
        weekday_mapping = {'Mo': 1, 'Tu': 2, 'We': 3,
            'Th': 4, 'Fr': 5, 'Sa': 6, 'Su': 7}
        iso_schedule = []
        for weekday in self.schedule.split(','):
            iso_schedule.append(weekday_mapping[weekday])
        return iso_schedule

    def datetime_in_time_zone(self):
        if self.time_zone is None:
            return None
        local_time_zone = - time.timezone // 3600
        hour_diff = local_time_zone - self.time_zone
        return dt.datetime.now() - dt.timedelta(hours=hour_diff)

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
