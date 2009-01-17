import datetime as dt
import feedparser
import mimetypes
import os
import re
import time
import urllib
import urlparse

from django.conf import settings
from django.db import transaction

from comics.common.models import Release, Strip
from comics.crawler.exceptions import *
from comics.crawler.utils.webparser import WebParser
from comics.utils.hash import sha256sum

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

        ### Populated by get_url()
        # Publication date
        self.pub_date = None
        # Strip website URL (optional)
        self.web_url = None
        # Strip feed URL (optional)
        self.feed_url = None
        # Strip URL (the result of get_url())
        self.url = None
        # Strip title (optional)
        self.title = None
        # Strip text (optional)
        self.text = None

        ### Populated by save_strip()
        # Strip relative filepath
        self.filename = None
        # Strip checksum
        self.checksum = None
        # The remote server response for debugging purposes
        self.response = None

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

    def parse_feed(self):
        if self.feed is None:
            self.feed = feedparser.parse(self.feed_url)

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

    @transaction.commit_manually
    def save_strip(self):
        """Download, sanitize and save strip"""

        # Download strip to temporary location
        tmpfilename = '%s/%s-%s.comics' % (
            '/var/tmp',
            self.comic.slug,
            self.pub_date.strftime('%Y-%m-%d'),
        )
        (tmpfilename, self.response) = urllib.urlretrieve(self.url, tmpfilename)
        urllib.urlcleanup()

        # Check if image based on mimetype
        if not self.response.getmaintype() == 'image':
            os.remove(tmpfilename)
            raise StripNotAnImage('%s/%s' % (self.comic.slug, self.pub_date))

        # Check if strip already exists based on checksum
        self.checksum = sha256sum(tmpfilename)
        if self.checksum in settings.COMICS_STRIP_BLACKLIST:
            raise CrawlerError('Strip blacklisted')
        try:
            strip = Strip.objects.get(comic=self.comic, checksum=self.checksum)
            os.remove(tmpfilename)
            if self.comic.has_reruns:
                return self.add_new_release(strip)
            else:
                raise StripAlreadyExists('Checksum collision')
        except Strip.DoesNotExist:
            pass

        # Detect file extension based on mimetype
        fileext = mimetypes.guess_extension(self.response.gettype())
        if fileext == '.jpe':
            fileext = '.jpg'

        # Construct final filename and path
        self.filename = '%(slug)s/%(year)d/%(date)s%(ext)s' % {
            'slug': self.comic.slug,
            'year': self.pub_date.year,
            'date': self.pub_date.strftime('%Y-%m-%d'),
            'ext': fileext,
        }
        fullpath = '%s%s' % (settings.MEDIA_ROOT, self.filename)
        (justpath, justfilename) = os.path.split(fullpath)

        # Create missing archive directories
        if not os.path.isdir(justpath):
            os.makedirs(justpath, 0755)

        # Move strip file to archive
        try:
            os.rename(tmpfilename, fullpath)
        except Exception, e:
            # Cleanup and re-raise error
            os.remove(tmpfilename)
            raise e

        # Create strip and release object
        strip = Strip(
            comic=self.comic, filename=self.filename, checksum=self.checksum)
        if self.title is not None:
            strip.title = self.title
        if self.text is not None:
            strip.text = self.text
        release = Release(
            comics=self.comic, pub_date=self.pub_date, strip=strip)

        # Save to database
        try:
            strip.save()
            release.save()
        except Exception, e:
            transaction.rollback()
            raise e
        else:
            transaction.commit()

    def add_new_release(self, strip):
        release = Release(
            comic=self.comic, pub_date=self.pub_date, strip=strip)
        try:
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
