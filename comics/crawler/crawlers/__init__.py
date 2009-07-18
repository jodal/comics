from __future__ import with_statement
import datetime as dt
import feedparser
import mimetypes
import os
import re
import shutil
import time
import urllib2
import urlparse

from django.conf import settings
from django.db import transaction

from comics.common.models import Comic, Release, Strip
from comics.crawler.exceptions import *
from comics.crawler.utils.webparser import WebParser
from comics.utils.hash import sha256sum

class BaseComicMeta(object):
    # Required values
    name = None
    language = None
    url = None

    # Default values
    start_date = None
    end_date = None
    history_capable_date = None
    history_capable_days = None
    has_reruns = False
    schedule = None
    time_zone = None
    rights = None

    @property
    def slug(self):
        return self.__module__.split('.')[-1]

    def create_comic(self):
        comic = Comic(
            name=self.name,
            slug=self.slug,
            language=self.language,
            url=self.url)
        if self.start_date:
            comic.start_date = self._get_date(self.start_date)
        if self.end_date:
            comic.end_date = self._get_date(self.end_date)
        if self.history_capable_date:
            comic.history_capable_date = self._get_date(
                self.history_capable_date)
        if self.history_capable_days:
            comic.history_capable_days = self.history_capable_days
        if self.has_reruns:
            comic.has_reruns = self.has_reruns
        if self.schedule:
            comic.schedule = self.schedule
        if self.time_zone:
            comic.time_zone = self.time_zone
        if self.rights:
            comic.rights = self.rights
        comic.save()

    def _get_date(self, date):
        return dt.datetime.strptime(date, '%Y-%m-%d').date()

class BaseComicCrawler(object):
    def __init__(self, comic):
        """Constructor"""

        # Database object for the comic
        self.comic = comic

        # Parsers for reuse through several calls to get_url()
        self.feed = None
        self.web_page = None

        self.reset()

    def reset(self):
        """Resets crawler state"""

        ### Populated during strip URL retrieval
        # Publication date
        self.pub_date = None
        # Strip website URL (optional)
        self.web_url = None
        # Strip URL (the result of get_url())
        self.url = None
        # Strip title (optional)
        self.title = None
        # Strip text (optional)
        self.text = None


    ### URL/title/text retrieval

    def get_url(self, pub_date=None):
        """Get URL of strip from pub_date, or the latest strip"""

        self._get_url_pre(pub_date)
        self._get_url()
        self._get_url_post()

    def _get_url_pre(self, pub_date=None):
        """Prepare crawler for a single strip crawl"""

        # Reset crawler state
        self.reset()

        # Strip publication date
        if pub_date is None:
            self.pub_date = dt.date.today()
        else:
            self.pub_date = pub_date

        if (not self.comic.history_capable()
            and not self.pub_date == dt.date.today()):
            raise NotHistoryCapable

        if (self.comic.history_capable() and
            self.pub_date < self.comic.history_capable()):
            raise OutsideHistoryCapabilityRange(
                'Not history capable, less than %s' %
                self.comic.history_capable())

        # XXX: With the following check, we do not support
        # multiple releases per comic per date
        if Release.objects.filter(comic=self.comic,
            pub_date=self.pub_date).count():
            raise StripAlreadyExists('%s/%s' % (self.comic.slug, self.pub_date))

    def _get_url(self):
        """Must be overridden by classes inheriting from BaseComicCrawler"""

        raise NotImplementedError

    def _get_url_post(self):
        """Validate URLs, titles and text gathered"""

        if not self.url:
            raise StripURLNotFound('%s/%s' % (self.comic.slug, self.pub_date))

        # Feed: Reencode title and text to UTF-8
        if (self.feed is not None
            and self.feed.encoding
            and self.feed.encoding != 'utf-8'):
            if self.title and type(self.title) != unicode:
                self.title = unicode(self.title, self.feed.encoding)
            if self.text and type(self.text) != unicode:
                self.text = unicode(self.text, self.feed.encoding)

        # Web: Reencode title and text to UTF-8
        if (self.web_page is not None
            and self.web_page.charset
            and self.web_page.charset != 'utf-8'):
            if self.title and type(self.title) != unicode:
                self.title = unicode(self.title, self.web_page.charset)
            if self.text and type(self.text) != unicode:
                self.text = unicode(self.text, self.web_page.charset)


    ### For use by subclasses in their _get_url() implementations

    def parse_feed(self, feed_url):
        if self.feed is None:
            self.feed = feedparser.parse(feed_url)

    def parse_web_page(self):
        if self.web_page is None:
            self.web_page = WebParser()
        self.web_page.parse_url(self.web_url)

    def join_web_url(self, relative_part):
        return urlparse.urljoin(self.web_url, relative_part)

    def timestamp_to_date(self, timestamp):
        return dt.date(*timestamp[:3])

    def string_to_date(self, *args, **kwargs):
        return dt.datetime.strptime(*args, **kwargs).date()

    def date_to_epoch(self, date):
        return int(time.mktime(date.timetuple()))

    def remove_html_tags(self, data):
        p = re.compile(r'<[^<]*?>')
        return p.sub('', data)


    ### Strip image retrieval

    def get_strip(self):
        """Download, sanitize and save strip"""

        assert self.pub_date is not None
        assert self.url is not None

        (temp_path, http_response) = self._download_strip_image()
        strip_checksum = sha256sum(temp_path)
        original_strip = self._get_strip_by_checksum(strip_checksum)

        if original_strip is not None:
            os.remove(temp_path)
            if self.comic.has_reruns:
                self._save_rerun_release(original_strip)
            else:
                raise StripAlreadyExists('Checksum collision')
        else:
            (absolute_path, relative_path) = self._get_image_path(http_response)
            self._archive_strip_image(temp_path, absolute_path)
            self._save_new_release(relative_path, strip_checksum)

    def _download_strip_image(self):
        """Download strip image to temporary location"""

        temp_path = '%s/%s-%s.comics' % (
            '/var/tmp',
            self.comic.slug,
            self.pub_date.strftime('%Y-%m-%d'),
        )

        request = urllib2.Request(self.url, None, self._get_headers())
        input_file = urllib2.urlopen(request)
        http_response = input_file.info()

        if not http_response.getmaintype() == 'image':
            input_file.close()
            raise StripNotAnImage('%s/%s' % (self.comic.slug, self.pub_date))

        with open(temp_path, 'wb') as temp_file:
            temp_file.write(input_file.read())

        input_file.close()

        return (temp_path, http_response)

    def _get_headers(self):
        return {}

    def _get_strip_by_checksum(self, strip_checksum):
        """Get existing strip based on checksum"""

        self._check_if_blacklisted(strip_checksum)
        try:
            return Strip.objects.get(comic=self.comic, checksum=strip_checksum)
        except Strip.DoesNotExist:
            return None

    def _check_if_blacklisted(self, strip_checksum):
        if strip_checksum in settings.COMICS_STRIP_BLACKLIST:
            raise CrawlerError('Strip blacklisted')

    def _get_image_path(self, http_response):
        # Detect file extension based on mimetype
        fileext = mimetypes.guess_extension(http_response.gettype())
        if fileext == '.jpe':
            fileext = '.jpg'

        # Construct final filename and path
        relative_path = '%(slug)s/%(year)d/%(date)s%(ext)s' % {
            'slug': self.comic.slug,
            'year': self.pub_date.year,
            'date': self.pub_date.strftime('%Y-%m-%d'),
            'ext': fileext,
        }
        absolute_path = '%s%s' % (settings.MEDIA_ROOT, relative_path)

        # Create missing archive directories
        (justpath, justfilename) = os.path.split(absolute_path)
        if not os.path.isdir(justpath):
            os.makedirs(justpath, 0755)

        return (absolute_path, relative_path)

    def _archive_strip_image(self, temp_path, archive_path):
        """Move strip file to archive"""

        try:
            shutil.move(temp_path, archive_path)
        except Exception, e:
            os.remove(temp_path)
            raise e

    def _save_new_release(self, relative_path, strip_checksum):
        strip = Strip(
            comic=self.comic, filename=relative_path, checksum=strip_checksum)
        if self.title is not None:
            strip.title = self.title
        if self.text is not None:
            strip.text = self.text
        self._save_strip_and_release(strip, new_release=True)

    def _save_rerun_release(self, strip):
        self._save_strip_and_release(strip, new_release=False)

    @transaction.commit_manually
    def _save_strip_and_release(self, strip, new_release=True):
        try:
            if new_release:
                strip.save()
            release = Release(
                comic=self.comic, pub_date=self.pub_date, strip=strip)
            release.save()
        except Exception, e:
            transaction.rollback()
            raise e
        else:
            transaction.commit()


class BaseComicsComComicCrawler(BaseComicCrawler):
    """Base comic crawler for all comics hosted at comics.com"""

    def _get_url_helper(self, comics_com_title):
        self.web_url = 'http://www.comics.com/%(slug)s/%(date)s/' % {
            'slug': comics_com_title.lower().replace(' ', '_'),
            'date': self.pub_date.strftime('%Y-%m-%d'),
        }

        self.parse_web_page()

        for img in self.web_page.imgs:
            if ('src' in img and 'alt' in img
                and img['alt'].startswith(comics_com_title)):
                self.url = self.join_web_url(img['src'])
                return
