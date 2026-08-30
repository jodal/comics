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


class ExpectedOutcome(AggregatorError):
    """Base class for the ways a crawl ends without a new release.

    These are the normal outcomes of crawling a comic we already have, or a
    date the comic did not publish on, and need nobody's attention.
    """


class TransientFailure(AggregatorError):
    """Base class for failures that may resolve on their own.

    The site was unreachable or misbehaved. Only a crawler that keeps failing
    this way needs repair, which a single crawl cannot tell.
    """


class CrawlerBroken(AggregatorError):
    """Base class for failures that need a human to repair the crawler.

    The site answered, but the crawler could not turn the answer into a
    release. That does not fix itself.
    """


###


class ReleaseAlreadyExists(ExpectedOutcome):
    """Exception raised when crawling a release that already exists"""

    def __str__(self) -> str:
        return f"{self.identifier}: Release already exists"


class BeforeHistoryStart(ExpectedOutcome):
    """Exception raised when crawling a date before the comic's history starts"""

    def __str__(self) -> str:
        return f"{self.identifier}: Date is before history start ({self.value})"


class ImageAlreadyExists(ExpectedOutcome):
    """Exception raised when trying to save an image that already exists"""

    def __str__(self) -> str:
        return f"{self.identifier}: Image already exists"


class ImageIsBlacklisted(ExpectedOutcome):
    """Exception raised when a blacklisted image has been downloaded"""

    def __str__(self) -> str:
        return f"{self.identifier}: Image is blacklisted"


###


class CrawlerHTTPError(TransientFailure):
    """Exception used to wrap HTTP errors from the crawler"""

    def __str__(self) -> str:
        return f"{self.identifier}: Crawler HTTP Error ({self.value})"


class DownloaderHTTPError(TransientFailure):
    """Exception used to wrap HTTP errors from the downloader"""

    def __str__(self) -> str:
        return f"{self.identifier}: Downloader HTTP Error ({self.value})"


###


class ImageURLNotFound(CrawlerBroken):
    """Exception raised when no URL is found by the crawler"""

    def __str__(self) -> str:
        return f"{self.identifier}: Image URL not found"


class ImageTypeError(CrawlerBroken):
    """Exception raised when the image isn't of the right type"""

    def __str__(self) -> str:
        return f"{self.identifier}: Invalid image type ({self.value})"


class ImageIsCorrupt(CrawlerBroken):
    """Exception raised when the fetched image is corrupt"""

    def __str__(self) -> str:
        return f"{self.identifier}: Image is corrupt ({self.value})"
