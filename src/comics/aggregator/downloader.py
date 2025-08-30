from __future__ import annotations

import hashlib
import tempfile
from typing import IO, TYPE_CHECKING

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
from comics.core.models import Comic, Image, Release

if TYPE_CHECKING:
    import datetime as dt

    from PIL.ImageFile import ImageFile as PILImageFile

    from comics.aggregator.crawler import CrawlerImage, CrawlerRelease

# Image types we accept, and the file extension they are saved with
IMAGE_FORMATS = {
    "GIF": ".gif",
    "JPEG": ".jpg",
    "PNG": ".png",
}


class ReleaseDownloader:
    def download(self, crawler_release: CrawlerRelease) -> Release:
        images = self._download_images(crawler_release)
        return self._create_new_release(
            crawler_release.comic, crawler_release.pub_date, images
        )

    def _download_images(self, crawler_release: CrawlerRelease) -> list[Image]:
        image_downloader = ImageDownloader(crawler_release)
        return list(map(image_downloader.download, crawler_release.images))

    @transaction.atomic
    def _create_new_release(
        self,
        comic: Comic,
        pub_date: dt.date,
        images: list[Image],
    ) -> Release:
        release = Release(comic=comic, pub_date=pub_date)
        release.save()
        for image in images:
            release.images.add(image)
        return release


class ImageDownloader:
    def __init__(self, crawler_release: CrawlerRelease) -> None:
        self.crawler_release = crawler_release

    def download(self, crawler_image: CrawlerImage) -> Image:
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

    def _download_image(
        self,
        url: str,
        request_headers: dict[str, str],
    ) -> IO[bytes]:
        try:
            response = httpx.get(url, headers=request_headers, follow_redirects=True)
            response.raise_for_status()
            temp_file = tempfile.NamedTemporaryFile(suffix="comics")
            temp_file.write(response.content)
            temp_file.seek(0)
        except (httpx.HTTPError, httpx.InvalidURL, OSError) as error:
            raise DownloaderHTTPError(self.identifier, error) from error
        else:
            return temp_file

    def _get_sha256sum(self, file_handle: IO[bytes]) -> str:
        original_position = file_handle.tell()
        h = hashlib.sha256()
        while True:
            data = file_handle.read(8096)
            if not data:
                break
            h.update(data)
        file_handle.seek(original_position)
        return h.hexdigest()

    def _check_if_blacklisted(self, checksum: str) -> None:
        if checksum in settings.COMICS_IMAGE_BLACKLIST:
            raise ImageIsBlacklisted(self.identifier)

    def _get_existing_image(
        self, comic: Comic, has_rerun_releases: bool, checksum: str
    ) -> Image | None:
        try:
            image = Image.objects.get(comic=comic, checksum=checksum)
        except Image.DoesNotExist:
            return None
        else:
            if not has_rerun_releases:
                raise ImageAlreadyExists(self.identifier)
            return image

    def _validate_image(self, image_file: IO[bytes]) -> PILImageFile:
        try:
            image = PILImage.open(image_file)
            image.load()  # pyright: ignore[reportUnknownMemberType]
        except IndexError as error:
            raise ImageIsCorrupt(self.identifier) from error
        except OSError as error:
            raise ImageIsCorrupt(self.identifier, error) from error
        else:
            return image

    def _get_file_extension(self, image: PILImageFile):
        if image.format not in IMAGE_FORMATS:
            raise ImageTypeError(self.identifier, image.format)
        return IMAGE_FORMATS[image.format]

    def _get_file_name(self, checksum: str, extension: str) -> str:
        if not (checksum and extension):
            raise ValueError("Checksum and extension must be non-empty")
        return f"{checksum}{extension}"

    @transaction.atomic
    def _create_new_image(
        self,
        comic: Comic,
        title: str | None,
        text: str | None,
        image_file: IO[bytes],
        file_name: str,
        checksum: str,
    ) -> Image:
        image = Image(comic=comic, checksum=checksum)
        image.file.save(file_name, File(image_file))
        if title is not None:
            image.title = title
        if text is not None:
            image.text = text
        image.save()
        return image
