from __future__ import with_statement
import mimetypes
import os
import shutil
import urllib2

from django.conf import settings
from django.db import transaction

from comics.aggregator.exceptions import *
from comics.core.models import Release, Strip
from comics.utils.hash import sha256sum

class ComicDownloader(object):
    def download_strip(self, strip_metadata):
        """Download, sanitize and save strip"""

        self.comic = strip_metadata['comic']
        self.check_image_mime_type = strip_metadata['check_image_mime_type']
        self.pub_date = strip_metadata['pub_date']
        self.url = strip_metadata['url']
        self.title = strip_metadata['title']
        self.text = strip_metadata['text']

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

        request = urllib2.Request(self.url, None, {})
        input_file = urllib2.urlopen(request)
        http_response = input_file.info()

        if (self.check_image_mime_type
                and not http_response.getmaintype() == 'image'):
            input_file.close()
            raise StripNotAnImage('%s/%s' % (self.comic.slug, self.pub_date))

        with open(temp_path, 'wb') as temp_file:
            temp_file.write(input_file.read())

        input_file.close()

        return (temp_path, http_response)

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
        absolute_path = '%s%s' % (settings.COMICS_MEDIA_ROOT, relative_path)

        # Create missing archive directories
        (justpath, justfilename) = os.path.split(absolute_path)
        if not os.path.isdir(justpath):
            os.makedirs(justpath, 0755)

        return (absolute_path, relative_path)

    def _archive_strip_image(self, temp_path, archive_path):
        try:
            shutil.move(temp_path, archive_path)
        except Exception:
            os.remove(temp_path)
            raise

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

    @transaction.commit_on_success
    def _save_strip_and_release(self, strip, new_release=True):
        if new_release:
            strip.save()
        release = Release(
            comic=self.comic, pub_date=self.pub_date, strip=strip)
        release.save()
