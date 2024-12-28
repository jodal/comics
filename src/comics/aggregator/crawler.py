from __future__ import annotations

import datetime
import re
import time
import xml.sax
import zoneinfo
from dataclasses import dataclass, field
from typing import TYPE_CHECKING

import httpx
from django.utils import timezone

from comics.aggregator.exceptions import (
    CrawlerHTTPError,
    ImageURLNotFound,
    NotHistoryCapable,
    ReleaseAlreadyExists,
)
from comics.aggregator.feedparser import FeedParser
from comics.aggregator.lxmlparser import LxmlParser

if TYPE_CHECKING:
    from comics.core.models import Comic

# For testability
now = timezone.now
today = datetime.date.today


RequestHeaders = dict[str, str]


@dataclass
class CrawlerRelease:
    comic: Comic
    pub_date: datetime.date
    has_rerun_releases: bool = False
    _images: list[CrawlerImage] = field(default_factory=list)

    @property
    def identifier(self) -> str:
        return f"{self.comic.slug}/{self.pub_date}"

    @property
    def images(self) -> list[CrawlerImage]:
        return self._images

    def add_image(self, image: CrawlerImage) -> None:
        image.validate(self.identifier)
        self._images.append(image)


@dataclass
class CrawlerImage:
    url: str
    title: str | None = None
    text: str | None = None
    request_headers: RequestHeaders = field(default_factory=dict)

    def __post_init__(self) -> None:
        # Convert from e.g. lxml.etree._ElementUnicodeResult to unicode
        if self.title is not None and not isinstance(self.title, str):
            self.title = str(self.title)
        if self.text is not None and not isinstance(self.text, str):
            self.text = str(self.text)

    def validate(self, identifier: str) -> None:
        if not self.url:
            raise ImageURLNotFound(identifier)


CrawlerResult = list[CrawlerImage] | CrawlerImage | None


@dataclass
class CrawlerBase:
    comic: Comic

    # ### Crawler settings
    # Date of oldest release available for crawling
    history_capable_date: str | None = field(init=False, default=None)
    # Number of days a release is available for crawling
    history_capable_days: int | None = field(init=False, default=None)
    # On what weekdays the comic is published (example: "Mo,We,Fr")
    schedule: str | None = field(init=False, default=None)
    # In approximately what time zone the comic is published
    # (example: "Europe/Oslo")
    time_zone: str = field(init=False, default="UTC")
    # Whether to allow multiple releases per day
    multiple_releases_per_day: bool = field(init=False, default=False)

    # ### Downloader settings
    # Whether the comic reruns old images as new releases
    has_rerun_releases: bool = field(init=False, default=False)

    # ### Settings used for both crawling and downloading
    # Dictionary of HTTP headers to send when retrieving items from the site
    headers: RequestHeaders = field(default_factory=dict)

    # Feed object which is reused when crawling multiple dates
    feed: FeedParser | None = None

    # Page objects mapped against URL for use when crawling multiple dates
    pages: dict[str, LxmlParser] = field(default_factory=dict)

    def get_crawler_release(
        self, pub_date: datetime.date | None = None
    ) -> CrawlerRelease | None:
        """Get meta data for release at pub_date, or the latest release"""

        pub_date = self._get_date_to_crawl(pub_date)
        release = CrawlerRelease(
            self.comic, pub_date, has_rerun_releases=self.has_rerun_releases
        )

        try:
            results = self.crawl(pub_date)
        except (httpx.HTTPError, httpx.InvalidURL, OSError) as error:
            raise CrawlerHTTPError(release.identifier, error) from error
        except xml.sax.SAXException as error:
            raise CrawlerHTTPError(release.identifier, str(error)) from error

        if not results:
            return None

        if isinstance(results, CrawlerImage):
            results = [results]

        for result in results:
            # Use HTTP headers when requesting images
            result.request_headers.update(self.headers)
            release.add_image(result)

        return release

    def _get_date_to_crawl(self, pub_date: datetime.date | None) -> datetime.date:
        identifier = f"{self.comic.slug}/{pub_date}"

        if pub_date is None:
            pub_date = self.current_date

        if pub_date < self.history_capable:
            raise NotHistoryCapable(identifier, self.history_capable)

        if (
            self.multiple_releases_per_day is False
            and self.comic.release_set.filter(pub_date=pub_date).count() > 0
        ):
            raise ReleaseAlreadyExists(identifier)

        return pub_date

    @property
    def current_date(self) -> datetime.date:
        time_zone = zoneinfo.ZoneInfo(self.time_zone)
        now_in_tz = now().astimezone(time_zone)
        return now_in_tz.date()

    @property
    def history_capable(self) -> datetime.date:
        if self.history_capable_date is not None:
            return datetime.datetime.strptime(
                self.history_capable_date, "%Y-%m-%d"
            ).date()
        elif self.history_capable_days is not None:
            return today() - datetime.timedelta(self.history_capable_days)
        else:
            return today()

    def crawl(self, pub_date: datetime.date) -> CrawlerResult:
        """
        Must be overridden by all crawlers

        Input:
            pub_date -- a datetime.date object for the date to crawl

        Output:
            on success: a CrawlResult object containing:
                - at least an image URL
                - optionally a title and/or a text
            on failure: None
        """

        raise NotImplementedError

    # ### Helpers for the crawl() implementations

    def parse_feed(self, feed_url: str) -> FeedParser:
        if self.feed is None:
            self.feed = FeedParser(feed_url)
        return self.feed

    def parse_page(self, page_url: str) -> LxmlParser:
        if page_url not in self.pages:
            self.pages[page_url] = LxmlParser(page_url, headers=self.headers)
        return self.pages[page_url]

    def string_to_date(self, string: str, fmt: str) -> datetime.date:
        return datetime.datetime.strptime(string, fmt).date()

    def date_to_epoch(self, date: datetime.date) -> int:
        """The UNIX time of midnight at ``date`` in the comic's time zone"""
        midnight = datetime.datetime(
            date.year, date.month, date.day, tzinfo=zoneinfo.ZoneInfo(self.time_zone)
        )
        return int(time.mktime(midnight.utctimetuple()))


class ComicsKingdomCrawlerBase(CrawlerBase):
    """Base comic crawler for Comics Kingdom comics"""

    def crawl_helper(self, short_name: str, pub_date: datetime.date) -> CrawlerResult:
        date = pub_date.strftime("%Y-%m-%d")
        page_url = f"https://comicskingdom.com/{short_name}/{date}"
        page = self.parse_page(page_url)
        url = page.src('img[id="theComicImage"]')
        if not url:
            url = page.content('meta[property="og:image"]')

        return CrawlerImage(url)


class GoComicsComCrawlerBase(CrawlerBase):
    """Base comic crawler for all comics hosted at gocomics.com"""

    # It doesn't want us getting comics because of a User-Agent check.
    # Look! I'm a nice, normal Internet Explorer machine!
    headers = {
        "User-Agent": (
            "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; "
            "Trident/4.0; .NET CLR 1.1.4322; .NET CLR 2.0.50727; "
            ".NET CLR 3.0.4506.2152; .NET CLR 3.5.30729"
        ),
    }

    def crawl_helper(self, url_name: str, pub_date: datetime.date) -> CrawlerResult:
        page_url = "http://www.gocomics.com/{}/{}".format(
            url_name,
            pub_date.strftime("%Y/%m/%d/"),
        )
        page = self.parse_page(page_url)
        url = page.src("picture.item-comic-image img")

        # If we request a date that doesn't exist
        # we get redirected to todays comic
        date = page.content('meta[property="article:published_time"]')
        if date != pub_date.strftime("%Y-%m-%d"):
            return None

        return CrawlerImage(url)


class PondusNoCrawlerBase(CrawlerBase):
    """Base comics crawler for all comics posted at pondus.no"""

    time_zone = "Europe/Oslo"

    def crawl_helper(self, url_id: str, pub_date: datetime.date) -> CrawlerResult:
        page_url = "http://www.pondus.no/?section=artikkel&id=%s" % url_id
        page = self.parse_page(page_url)
        url = page.src(".imagegallery img")
        return CrawlerImage(url)


class DagbladetCrawlerBase(CrawlerBase):
    """Base comics crawler for all comics posted at dagbladet.no"""

    headers = {"User-Agent": "Mozilla/5.0"}
    time_zone = "Europe/Oslo"

    def crawl_helper(self, short_name: str, pub_date: datetime.date) -> CrawlerResult:
        page_url = "http://www.dagbladet.no/tegneserie/%s" % short_name
        page = self.parse_page(page_url)

        date_string = pub_date.strftime("%Y-%m-%dT00:00:00")
        time = page.root.xpath('//time[contains(@datetime,"%s")]' % date_string)

        if not time:
            return None

        article = time[0].getparent().getparent()
        url = article.find(".//img").get("src")
        url = url.replace("_1000", "")

        return CrawlerImage(url)


class CreatorsCrawlerBase(CrawlerBase):
    """Base comics crawler for all comics posted at creators.com"""

    headers = {"User-Agent": "Mozilla/5.0"}

    def crawl_helper(self, feature_id: str, pub_date: datetime.date) -> CrawlerResult:
        url = (
            "https://www.creators.com/api/features/get_release_dates?"
            "feature_id=%s&year=%s"
        ) % (feature_id, pub_date.year)

        response = httpx.get(url, headers=self.headers, follow_redirects=True)
        releases = response.json()

        for release in releases:
            if release["release"] == pub_date.strftime("%Y-%m-%d"):
                page = self.parse_page(release["url"])
                url = page.src('img[itemprop="image"]')
                return CrawlerImage(url)

        return None


class NettserierCrawlerBase(CrawlerBase):
    """Base comics crawler for all comics posted at nettserier.no"""

    # Nettserier has no option to fetch a specific date
    # In order to get older releases we need to
    # loop through the pages and check the published date
    time_zone = "Europe/Oslo"
    page_cache: dict[str, tuple[LxmlParser, datetime.date]] = {}

    def get_page(self, url: str) -> tuple[LxmlParser, datetime.date]:
        if url not in self.page_cache:
            page = self.parse_page(url)
            page_date = page.text('p[class="comic-pubtime"]')
            date = self.string_to_date(page_date, "Published %Y-%m-%d %H:%M:%S")
            self.page_cache[url] = (page, date)
        return self.page_cache[url]

    def crawl_helper(self, short_name: str, pub_date: datetime.date) -> CrawlerResult:
        url = "https://nettserier.no/%s/" % short_name
        page, comic_date = self.get_page(url)

        while pub_date < comic_date:
            # Wanted date is earlier than the current, get previous page
            previous_link = page.root.xpath('//li[@class="prev"]/a/@href')
            if not previous_link:
                return None  # No previous comic
            page, comic_date = self.get_page(previous_link[0])

        if pub_date != comic_date:
            return None  # Correct date not found

        # comic-text div which contains title and text for the comic
        title = page.text("div.comic-text h4")
        text = page.text("div.comic-text p", allow_multiple=True)

        text = None if text[0].find("Published") > -1 else text[0]

        # Get comic image
        url = page.src('img[src*="/_ns/files"]')
        return CrawlerImage(url, title, text)


class ComicControlCrawlerBase(CrawlerBase):
    """Base comics crawler for all comics using ComicControl CMS"""

    def crawl_helper(self, site_url: str, pub_date: datetime.date) -> CrawlerResult:
        if site_url[-1] == "/":
            site_url = site_url[0:-1]
        if "pixietrixcomix.com" in site_url:
            feed = self.parse_feed("%s/rss" % site_url)
        else:
            feed = self.parse_feed("%s/comic/rss" % site_url)

        for entry in feed.for_date(pub_date):
            page = self.parse_page(entry.link)
            url = page.src("img#cc-comic")
            text = page.title("img#cc-comic")
            title = re.sub(r".+? - (.+)", r"\1", entry.title)

            return CrawlerImage(url, title, text)

        return None
