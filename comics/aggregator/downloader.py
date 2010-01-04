from __future__ import with_statement
import mimetypes
import tempfile
import urllib2

from django.conf import settings
from django.core.files import File
from django.db import transaction

from comics.aggregator.exceptions import (FileNotAnImage, DownloaderHTTPError,
    ImageAlreadyExists, ImageIsBlacklisted)
from comics.core.models import Release, Strip
from comics.utils.hash import sha256sum

class Downloader(object):
    def download_strip(self, strip_meta):
        (image, filename, checksum) = self._download_image(strip_meta)
        original_strip = self._get_strip_by_checksum(strip_meta, checksum)
        if original_strip is not None and strip_meta.has_rerun_releases:
            self._save_rerun_release(strip_meta, original_strip)
        elif original_strip is not None and not strip_meta.has_rerun_releases:
            raise ImageAlreadyExists(strip_meta.identifier)
        else:
            self._save_new_release(strip_meta, image, filename, checksum)

    def _download_image(self, strip_meta):
        try:
            request = urllib2.Request(strip_meta.url, None,
                strip_meta.request_headers)
            http_file = urllib2.urlopen(request)
            self._check_image_mime_type(strip_meta, http_file)
            image = self._get_temporary_file(http_file)
            checksum = sha256sum(filehandle=image)
            self._check_if_blacklisted(strip_meta, checksum)
            filename = '%s%s' % (checksum, self._get_file_extension(http_file))
            http_file.close()
            return (File(image), filename, checksum)
        except urllib2.HTTPError, error:
            raise DownloaderHTTPError(strip_meta.identifier, error)

    def _check_image_mime_type(self, strip_meta, http_file):
        if (strip_meta.check_image_mime_type
                and not http_file.info().getmaintype() == 'image'):
            raise FileNotAnImage(strip_meta.identifier)

    def _get_temporary_file(self, source_file):
        tmp = tempfile.NamedTemporaryFile(suffix='comics')
        tmp.write(source_file.read())
        tmp.seek(0)
        return tmp

    def _get_file_extension(self, http_file):
        file_ext = mimetypes.guess_extension(http_file.info().gettype())
        if file_ext == '.jpe':
            file_ext = '.jpg'
        return file_ext

    def _check_if_blacklisted(self, strip_meta, checksum):
        if checksum in settings.COMICS_STRIP_BLACKLIST:
            raise ImageIsBlacklisted(strip_meta.identifier)

    def _get_strip_by_checksum(self, strip_meta, checksum):
        try:
            return Strip.objects.get(comic=strip_meta.comic,
                checksum=checksum)
        except Strip.DoesNotExist:
            return None

    def _save_new_release(self, strip_meta, image, filename, checksum):
        strip = Strip(comic=strip_meta.comic, checksum=checksum)
        strip.file.save(filename, image)
        if strip_meta.title is not None:
            strip.title = strip_meta.title
        if strip_meta.text is not None:
            strip.text = strip_meta.text
        self._save_strip_and_release(strip_meta, strip, new_release=True)

    def _save_rerun_release(self, strip_meta, strip):
        self._save_strip_and_release(strip_meta, strip, new_release=False)

    @transaction.commit_on_success
    def _save_strip_and_release(self, strip_meta, strip, new_release=True):
        if new_release:
            strip.save()
        release = Release(
            comic=strip_meta.comic,
            pub_date=strip_meta.pub_date,
            strip=strip)
        release.save()
