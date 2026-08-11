"""Aggregator which fetches comic releases from the web"""

from __future__ import annotations

import datetime as dt
import functools
import logging
import socket
import time
from typing import TYPE_CHECKING, Concatenate

from comics.aggregator.downloader import ReleaseDownloader
from comics.comics import get_comic_crawler
from comics.core.exceptions import ComicsError
from comics.core.models import Comic

if TYPE_CHECKING:
    from collections.abc import Callable

    from comics.aggregator.crawler import CrawlerBase, CrawlerRelease

logger = logging.getLogger("comics.aggregator.command")
socket.setdefaulttimeout(10)


def log_errors[**P, R](
    func: Callable[Concatenate[Aggregator, P], R],
) -> Callable[Concatenate[Aggregator, P], R | None]:
    @functools.wraps(func)
    def inner(aggregator: Aggregator, *args: P.args, **kwargs: P.kwargs) -> R | None:
        try:
            return func(aggregator, *args, **kwargs)
        except ComicsError as error:
            logger.info(error)
            return None
        except Exception as error:
            logger.exception("%s: %s", aggregator.identifier, error)
            return None

    return inner


def select_comics(requested: list[str]) -> list[Comic]:
    """The comics to crawl.

    Without any requested comics, or with `"all"`, every comic in the
    database is selected. An unknown slug is an error rather than a comic
    quietly missing from the crawl.
    """
    if len(requested) == 0 or "all" in requested:
        logger.debug("Crawl targets: all comics")
        return list(Comic.objects.all())

    comics = [_get_comic_by_slug(comic_slug) for comic_slug in requested]
    logger.debug("Crawl targets: %s", comics)
    return comics


def _get_comic_by_slug(comic_slug: str) -> Comic:
    comic = Comic.objects.for_slugs(comic_slug).get_or_none()
    if comic is None:
        error_msg = f"Comic {comic_slug} not found"
        logger.error(error_msg)
        raise ComicsError(error_msg)
    return comic


def parse_date_range(
    from_date: dt.date | str | None,
    to_date: dt.date | str | None,
) -> tuple[dt.date | None, dt.date | None]:
    """The dates to crawl between, parsing ISO 8601 date strings."""
    if isinstance(from_date, str):
        from_date = dt.date.fromisoformat(from_date)
    logger.debug("From date: %s", from_date)

    if isinstance(to_date, str):
        to_date = dt.date.fromisoformat(to_date)
    logger.debug("To date: %s", to_date)

    if from_date and to_date and from_date > to_date:
        error_msg = f"From date ({from_date}) after to date ({to_date})"
        logger.error(error_msg)
        raise ComicsError(error_msg)

    return from_date, to_date


class Aggregator:
    identifier: str | None = None

    def __init__(
        self,
        comics: list[Comic],
        from_date: dt.date | None = None,
        to_date: dt.date | None = None,
    ) -> None:
        self.comics = comics
        self.from_date = from_date
        self.to_date = to_date

    def start(self) -> None:
        start_time = time.monotonic()
        for comic in self.comics:
            self.identifier = comic.slug
            self._aggregate_one_comic(comic)
        elapsed_time = dt.timedelta(seconds=time.monotonic() - start_time)
        logger.info("Crawling completed in %s", elapsed_time)

    @log_errors
    def _aggregate_one_comic(self, comic: Comic) -> None:
        crawler = get_comic_crawler(comic)
        if crawler is None:
            logger.info("%s: No crawler defined, skipping", comic.slug)
            return

        from_date = self._get_valid_date(crawler, self.from_date)
        to_date = self._get_valid_date(crawler, self.to_date)
        if from_date != to_date:
            logger.info("%s: Crawling from %s to %s", comic.slug, from_date, to_date)
        pub_date = from_date
        while pub_date <= to_date:
            self.identifier = f"{comic.slug}/{pub_date}"
            crawler_release = self._crawl_one_comic_one_date(crawler, pub_date)
            if crawler_release:
                self._download_release(crawler_release)
            else:
                logger.info("%s: No release found", self.identifier)
            pub_date += dt.timedelta(days=1)

    @log_errors
    def _crawl_one_comic_one_date(
        self,
        crawler: CrawlerBase,
        pub_date: dt.date,
    ) -> CrawlerRelease | None:
        logger.debug("Crawling %s for %s", crawler.comic.slug, pub_date)
        crawler_release = crawler.get_release(pub_date)
        if crawler_release:
            logger.debug("Release: %s", crawler_release.identifier)
            for image in crawler_release.images:
                logger.debug("Image URL: %s", image.url)
                logger.debug("Image title: %s", image.title)
                logger.debug("Image text: %s", image.text)
        return crawler_release

    @log_errors
    def _download_release(self, crawler_release: CrawlerRelease) -> None:
        logger.debug("Downloading %s", crawler_release.identifier)
        downloader = self._get_downloader()
        downloader.download(crawler_release)
        logger.info("%s: Release saved", crawler_release.identifier)

    def _get_downloader(self) -> ReleaseDownloader:
        return ReleaseDownloader()

    def _get_valid_date(self, crawler: CrawlerBase, date: dt.date | None) -> dt.date:
        if date is None:
            return crawler.current_date
        elif date < crawler.history_start:
            logger.info(
                "%s: Adjusting date from %s to %s because the given "
                "date is before the comic's history start",
                crawler.comic.slug,
                date,
                crawler.history_start,
            )
            return crawler.history_start
        elif date > crawler.current_date:
            logger.info(
                "%s: Adjusting date from %s to %s because the given "
                "date is in the future in the comic's time zone",
                crawler.comic.slug,
                date,
                crawler.current_date,
            )
            return crawler.current_date
        else:
            return date
