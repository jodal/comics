from __future__ import annotations

import tempfile
from typing import IO, TYPE_CHECKING

import httpx

# Importing the plugin registers the JPEG XL codec with Pillow
import pillow_jxl  # noqa: F401  # pyright: ignore[reportUnusedImport]
from django.conf import settings
from django.core.files import File
from PIL import Image as PILImage

from comics.aggregator.exceptions import (
    DownloaderHTTPError,
    ImageAlreadyExists,
    ImageIsBlacklisted,
    ImageIsCorrupt,
    ImageTypeError,
)
from comics.core.files import sha256sum
from comics.core.models import Comic, Image, Release
from comics.core.services import ImageService, ReleaseService

if TYPE_CHECKING:
    from PIL.ImageFile import ImageFile as PILImageFile

    from comics.aggregator.crawler import CrawlerImage, CrawlerRelease

# Image types we accept, and the file extension they are saved with
IMAGE_FORMATS = {
    "AVIF": ".avif",
    "GIF": ".gif",
    "JPEG": ".jpg",
    "JXL": ".jxl",
    "PNG": ".png",
    "WEBP": ".webp",
}


class ReleaseDownloader:
    def download(self, crawler_release: CrawlerRelease) -> Release:
        images = self._download_images(crawler_release)
        return ReleaseService.create(
            comic=crawler_release.comic,
            pub_date=crawler_release.pub_date,
            images=images,
        )

    def _download_images(self, crawler_release: CrawlerRelease) -> list[Image]:
        image_downloader = ImageDownloader(crawler_release)
        return list(map(image_downloader.download, crawler_release.images))


class ImageDownloader:
    def __init__(self, crawler_release: CrawlerRelease) -> None:
        self.crawler_release = crawler_release

    def download(self, crawler_image: CrawlerImage) -> Image:
        self.identifier = self.crawler_release.identifier

        # CrawlerRelease.add_image() has validated that the URL is present.
        assert crawler_image.url is not None

        with self._download_image(
            crawler_image.url, crawler_image.request_headers
        ) as image_file:
            file = File(image_file)
            checksum = sha256sum(file)
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

            return ImageService.create(
                comic=self.crawler_release.comic,
                file=file,
                file_extension=self._get_file_extension(image),
                title=crawler_image.title,
                text=crawler_image.text,
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

    def _check_if_blacklisted(self, checksum: str) -> None:
        if checksum in settings.COMICS_IMAGE_BLACKLIST:
            raise ImageIsBlacklisted(self.identifier)

    def _get_existing_image(
        self,
        comic: Comic,
        has_rerun_releases: bool,
        checksum: str,
    ) -> Image | None:
        image = Image.objects.for_comics(comic).for_checksum(checksum).get_or_none()
        if image is not None and not has_rerun_releases:
            raise ImageAlreadyExists(self.identifier)
        return image

    def _validate_image(self, image_file: IO[bytes]) -> PILImageFile:
        try:
            image = PILImage.open(image_file)
            image.load()
        except IndexError as error:
            raise ImageIsCorrupt(self.identifier) from error
        except OSError as error:
            raise ImageIsCorrupt(self.identifier, error) from error
        else:
            return image

    def _get_file_extension(self, image: PILImageFile) -> str:
        if image.format not in IMAGE_FORMATS:
            raise ImageTypeError(self.identifier, image.format)
        return IMAGE_FORMATS[image.format]
