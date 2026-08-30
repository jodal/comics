import datetime as dt

from comics.core.exceptions import ComicsError


class AggregatorError(ComicsError):
    """base class for aggregator exceptions"""

    def __init__(
        self,
        *,
        slug: str,
        pub_date: dt.date,
        value: object = None,
        detail: str | None = None,
    ) -> None:
        self.slug = slug
        self.pub_date = pub_date
        self.value = value
        self.detail = detail

    @property
    def identifier(self) -> str:
        parts = [self.slug, str(self.pub_date)]
        if self.detail is not None:
            parts.append(self.detail)
        return "/".join(parts)

    def __str__(self) -> str:
        return f"{self.identifier}: Generic aggregator error"


###


class CrawlerError(AggregatorError):
    """Base class for crawler exceptions"""

    def __str__(self) -> str:
        return f"{self.identifier}: Generic crawler error ({self.value})"


class CrawlerHTTPError(CrawlerError):
    """Exception used to wrap HTTP errors from the crawler"""

    def __str__(self) -> str:
        return f"{self.identifier}: Crawler HTTP Error ({self.value})"


class ImageURLNotFound(CrawlerError):
    """Exception raised when no URL is found by the crawler"""

    def __str__(self) -> str:
        return f"{self.identifier}: Image URL not found"


class BeforeHistoryStart(CrawlerError):
    """Exception raised when crawling a date before the comic's history starts"""

    def __str__(self) -> str:
        return f"{self.identifier}: Date is before history start ({self.value})"


class ReleaseAlreadyExists(CrawlerError):
    """Exception raised when crawling a release that already exists"""

    def __str__(self) -> str:
        return f"{self.identifier}: Release already exists"


###


class DownloaderError(AggregatorError):
    """Base class for downloader exceptions"""

    def __str__(self) -> str:
        return f"{self.identifier}: Generic downloader error ({self.value})"


class DownloaderHTTPError(DownloaderError):
    """Exception used to wrap HTTP errors from the downloader"""

    def __str__(self) -> str:
        return f"{self.identifier}: Downloader HTTP Error ({self.value})"


class ImageTypeError(DownloaderError):
    """Exception raised when the image isn't of the right type"""

    def __str__(self) -> str:
        return f"{self.identifier}: Invalid image type ({self.value})"


class ImageIsCorrupt(DownloaderError):
    """Exception raised when the fetched image is corrupt"""

    def __str__(self) -> str:
        return f"{self.identifier}: Image is corrupt ({self.value})"


class ImageAlreadyExists(DownloaderError):
    """Exception raised when trying to save an image that already exists"""

    def __str__(self) -> str:
        return f"{self.identifier}: Image already exists"


class ImageIsBlacklisted(DownloaderError):
    """Exception raised when a blacklisted image has been downloaded"""

    def __str__(self) -> str:
        return f"{self.identifier}: Image is blacklisted"
