from __future__ import with_statement
import mimetypes
import os
import shutil
import urllib2

from django.conf import settings
from django.db import transaction

from comics.aggregator.exceptions import (FileNotAnImage, DownloaderHTTPError,
    ImageAlreadyExists)
from comics.core.models import Release, Strip
from comics.utils.hash import sha256sum

class Downloader(object):
    def download_strip(self, strip_metadata):
        """Download, sanitize and save strip"""

        (temp_path, http_response) = self._download_strip_image(strip_metadata)
        strip_checksum = sha256sum(temp_path)
        original_strip = self._get_strip_by_checksum(strip_metadata.comic,
            strip_checksum)

        if original_strip is not None:
            os.remove(temp_path)
            if strip_metadata.has_rerun_releases:
                self._save_rerun_release(strip_metadata.comic,
                    strip_metadata.pub_date, original_strip)
            else:
                raise ImageAlreadyExists(strip_metadata.identifier)
        else:
            (absolute_path, relative_path) = self._get_image_path(
                strip_metadata, http_response)
            self._archive_strip_image(temp_path, absolute_path)
            self._save_new_release(strip_metadata, relative_path,
                strip_checksum)

    def _download_strip_image(self, strip_metadata):
        """Download strip image to temporary location"""

        try:
            temp_path = '%s/%s-%s.comics' % (
                '/var/tmp',
                strip_metadata.comic.slug,
                strip_metadata.pub_date.strftime('%Y-%m-%d'),
            )

            request = urllib2.Request(strip_metadata.url, None,
                strip_metadata.request_headers)
            input_file = urllib2.urlopen(request)
            http_response = input_file.info()

            if (strip_metadata.check_image_mime_type
                    and not http_response.getmaintype() == 'image'):
                input_file.close()
                raise FileNotAnImage(strip_metadata.identifier)

            with open(temp_path, 'wb') as temp_file:
                temp_file.write(input_file.read())

            input_file.close()

            return (temp_path, http_response)
        except urllib2.HTTPError, error:
            raise DownloaderHTTPError(strip_metadata.identifier, error)

    def _get_strip_by_checksum(self, comic, strip_checksum):
        """Get existing strip based on checksum"""

        self._check_if_blacklisted(strip_checksum)
        try:
            return Strip.objects.get(comic=comic, checksum=strip_checksum)
        except Strip.DoesNotExist:
            return None

    def _check_if_blacklisted(self, strip_checksum):
        if strip_checksum in settings.COMICS_STRIP_BLACKLIST:
            raise CrawlerError('Strip blacklisted')

    def _get_image_path(self, strip_metadata, http_response):
        # Detect file extension based on mimetype
        fileext = mimetypes.guess_extension(http_response.gettype())
        if fileext == '.jpe':
            fileext = '.jpg'

        # Construct final filename and path
        relative_path = '%(slug)s/%(year)d/%(date)s%(ext)s' % {
            'slug': strip_metadata.comic.slug,
            'year': strip_metadata.pub_date.year,
            'date': strip_metadata.pub_date.strftime('%Y-%m-%d'),
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

    def _save_new_release(self, strip_metadata, relative_path, strip_checksum):
        strip = Strip(comic=strip_metadata.comic, filename=relative_path,
            checksum=strip_checksum)
        if strip_metadata.title is not None:
            strip.title = strip_metadata.title
        if strip_metadata.text is not None:
            strip.text = strip_metadata.text
        self._save_strip_and_release(strip_metadata.comic,
            strip_metadata.pub_date, strip, new_release=True)

    def _save_rerun_release(self, comic, pub_date, strip):
        self._save_strip_and_release(comic, pub_date, strip, new_release=False)

    @transaction.commit_on_success
    def _save_strip_and_release(self, comic, pub_date, strip, new_release=True):
        if new_release:
            strip.save()
        release = Release(comic=comic, pub_date=pub_date, strip=strip)
        release.save()
