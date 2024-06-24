import hashlib
import tempfile

import httpx
from django.conf import settings
from django.core.files import File
from django.db import transaction
from PIL import Image as PILImage

from comics.aggregator.exceptions import (
    DownloaderHTTPError,
    ImageAlreadyExists,
    ImageIsBlacklisted,
    ImageIsCorrupt,
    ImageTypeError,
)
from comics.core.models import Image, Release

# Image types we accept, and the file extension they are saved with
IMAGE_FORMATS = {
    "GIF": ".gif",
    "JPEG": ".jpg",
    "PNG": ".png",
}


class ReleaseDownloader:
    def download(self, crawler_release):
        images = self._download_images(crawler_release)
        return self._create_new_release(
            crawler_release.comic, crawler_release.pub_date, images
        )

    def _download_images(self, crawler_release):
        image_downloader = ImageDownloader(crawler_release)
        return list(map(image_downloader.download, crawler_release.images))

    @transaction.atomic
    def _create_new_release(self, comic, pub_date, images):
        release = Release(comic=comic, pub_date=pub_date)
        release.save()
        for image in images:
            release.images.add(image)
        return release


class ImageDownloader:
    def __init__(self, crawler_release):
        self.crawler_release = crawler_release

    def download(self, crawler_image):
        self.identifier = self.crawler_release.identifier

        with self._download_image(
            crawler_image.url, crawler_image.request_headers
        ) as image_file:
            checksum = self._get_sha256sum(image_file)
            self.identifier = f"{self.identifier}/{checksum[:6]}"

            self._check_if_blacklisted(checksum)

            existing_image = self._get_existing_image(
                comic=self.crawler_release.comic,
                has_rerun_releases=self.crawler_release.has_rerun_releases,
                checksum=checksum,
            )
            if existing_image is not None:
                return existing_image

            image = self._validate_image(image_file)

            file_extension = self._get_file_extension(image)
            file_name = self._get_file_name(checksum, file_extension)

            return self._create_new_image(
                comic=self.crawler_release.comic,
                title=crawler_image.title,
                text=crawler_image.text,
                image_file=image_file,
                file_name=file_name,
                checksum=checksum,
            )

    def _download_image(self, url, request_headers):
        try:
            response = httpx.get(url, headers=request_headers, follow_redirects=True)
            response.raise_for_status()
            temp_file = tempfile.NamedTemporaryFile(suffix="comics")
            temp_file.write(response.content)
            temp_file.seek(0)
            return temp_file
        except (httpx.HTTPError, httpx.InvalidURL, OSError) as error:
            raise DownloaderHTTPError(self.identifier, error)

    def _get_sha256sum(self, file_handle):
        original_position = file_handle.tell()
        hash = hashlib.sha256()
        while True:
            data = file_handle.read(8096)
            if not data:
                break
            hash.update(data)
        file_handle.seek(original_position)
        return hash.hexdigest()

    def _check_if_blacklisted(self, checksum):
        if checksum in settings.COMICS_IMAGE_BLACKLIST:
            raise ImageIsBlacklisted(self.identifier)

    def _get_existing_image(self, comic, has_rerun_releases, checksum):
        try:
            image = Image.objects.get(comic=comic, checksum=checksum)
            if image is not None and not has_rerun_releases:
                raise ImageAlreadyExists(self.identifier)
            return image
        except Image.DoesNotExist:
            return None

    def _validate_image(self, image_file):
        try:
            image = PILImage.open(image_file)
            image.load()
            return image
        except IndexError:
            raise ImageIsCorrupt(self.identifier)
        except OSError as error:
            raise ImageIsCorrupt(self.identifier, error)

    def _get_file_extension(self, image):
        if image.format not in IMAGE_FORMATS:
            raise ImageTypeError(self.identifier, image.format)
        return IMAGE_FORMATS[image.format]

    def _get_file_name(self, checksum, extension):
        if checksum and extension:
            return f"{checksum}{extension}"

    @transaction.atomic
    def _create_new_image(self, comic, title, text, image_file, file_name, checksum):
        image = Image(comic=comic, checksum=checksum)
        image.file.save(file_name, File(image_file))
        if title is not None:
            image.title = title
        if text is not None:
            image.text = text
        image.save()
        return image
