from __future__ import with_statement
import mimetypes
import tempfile
import urllib2

from django.conf import settings
from django.core.files import File
from django.db import transaction

from comics.aggregator.exceptions import (FileNotAnImage, DownloaderHTTPError,
    ImageAlreadyExists, ImageIsBlacklisted)
from comics.core.models import Release, Image
from comics.utils.hash import sha256sum

class Downloader(object):
    def download_release(self, release_meta):
        (image, filename, checksum) = self._download_image(release_meta)
        original_image = self._get_image_by_checksum(release_meta, checksum)
        if original_image is not None and release_meta.has_rerun_releases:
            self._save_rerun_release(release_meta, original_image)
        elif original_image is not None and not release_meta.has_rerun_releases:
            raise ImageAlreadyExists(release_meta.identifier)
        else:
            self._save_new_release(release_meta, image, filename, checksum)

    def _download_image(self, release_meta):
        try:
            request = urllib2.Request(release_meta.url, None,
                release_meta.request_headers)
            http_file = urllib2.urlopen(request)
            self._check_image_mime_type(release_meta, http_file)
            image = self._get_temporary_file(http_file)
            checksum = sha256sum(filehandle=image)
            self._check_if_blacklisted(release_meta, checksum)
            filename = '%s%s' % (checksum, self._get_file_extension(http_file))
            http_file.close()
            return (File(image), filename, checksum)
        except urllib2.HTTPError, error:
            raise DownloaderHTTPError(release_meta.identifier, error)

    def _check_image_mime_type(self, release_meta, http_file):
        if (release_meta.check_image_mime_type
                and not http_file.info().getmaintype() == 'image'):
            raise FileNotAnImage(release_meta.identifier)

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

    def _check_if_blacklisted(self, release_meta, checksum):
        if checksum in settings.COMICS_IMAGE_BLACKLIST:
            raise ImageIsBlacklisted(release_meta.identifier)

    def _get_image_by_checksum(self, release_meta, checksum):
        try:
            return Image.objects.get(comic=release_meta.comic,
                checksum=checksum)
        except Image.DoesNotExist:
            return None

    def _save_new_release(self, release_meta, image_file, filename, checksum):
        image = Image(comic=release_meta.comic, checksum=checksum)
        image.file.save(filename, image_file)
        if release_meta.title is not None:
            image.title = release_meta.title
        if release_meta.text is not None:
            image.text = release_meta.text
        self._save_image_and_release(release_meta, image, new_release=True)

    def _save_rerun_release(self, release_meta, image):
        self._save_image_and_release(release_meta, image, new_release=False)

    @transaction.commit_on_success
    def _save_image_and_release(self, release_meta, image, new_release=True):
        if new_release:
            image.save()
        release = Release(
            comic=release_meta.comic, pub_date=release_meta.pub_date)
        release.save()
        release.images.add(image)
