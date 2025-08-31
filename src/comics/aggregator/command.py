"""Aggregator which fetches comic releases from the web"""

from __future__ import annotations

import datetime as dt
import functools
import logging
import socket
from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Any, Concatenate, Self

from comics.aggregator.downloader import ReleaseDownloader
from comics.comics import get_comic_crawler
from comics.core.exceptions import ComicsError

if TYPE_CHECKING:
    from collections.abc import Callable

    from comics.aggregator.crawler import CrawlerBase, CrawlerRelease
    from comics.core.models import Comic

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


class Aggregator:
    config: AggregatorConfig
    identifier: str | None = None

    def __init__(
        self,
        config: AggregatorConfig | None = None,
        options: dict[str, Any] | None = None,
    ):
        if config is None and options is not None:
            self.config = AggregatorConfig.from_options(**options)
        else:
            assert isinstance(config, AggregatorConfig)
            self.config = config

    def start(self):
        start_time = dt.datetime.now()
        for comic in self.config.comics:
            self.identifier = comic.slug
            self._aggregate_one_comic(comic)
        elapsed_time = dt.datetime.now() - start_time
        logger.info("Crawling completed in %s", elapsed_time)

    def stop(self):
        pass

    @log_errors
    def _aggregate_one_comic(self, comic: Comic) -> None:
        crawler = get_comic_crawler(comic)
        if crawler is None:
            logger.info("%s: No crawler defined, skipping", comic.slug)
            return

        from_date = self._get_valid_date(crawler, self.config.from_date)
        to_date = self._get_valid_date(crawler, self.config.to_date)
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
        crawler_release = crawler.get_crawler_release(pub_date)
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
        elif date < crawler.history_capable:
            logger.info(
                "%s: Adjusting date from %s to %s because of "
                "limited history capability",
                crawler.comic.slug,
                date,
                crawler.history_capable,
            )
            return crawler.history_capable
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


@dataclass
class AggregatorConfig:
    DATE_FORMAT = "%Y-%m-%d"

    comic_slugs: list[str] = field(default_factory=list)
    from_date: dt.date | None = None
    to_date: dt.date | None = None

    @classmethod
    def from_options(cls, **options: Any) -> Self:
        from_date, to_date = cls._get_date_interval(
            options.get("from_date"),
            options.get("to_date"),
        )
        return cls(
            comic_slugs=options.get("comic_slugs") or [],
            from_date=from_date,
            to_date=to_date,
        )

    @property
    def comics(self) -> list[Comic]:
        from comics.core.models import Comic  # noqa: PLC0415

        if len(self.comic_slugs) == 0:
            logger.debug("Crawl targets: all comics")
            return list(Comic.objects.all())
        else:
            comics = [self._get_comic_by_slug(slug) for slug in self.comic_slugs]
            logger.debug("Crawl targets: %s", comics)
            return comics

    @classmethod
    def _get_comic_by_slug(cls, comic_slug: str) -> Comic:
        from comics.core.models import Comic  # noqa: PLC0415

        try:
            comic = Comic.objects.get(slug=comic_slug)
        except Comic.DoesNotExist as exc:
            error_msg = "Comic %s not found" % comic_slug
            logger.error(error_msg)
            raise ComicsError(error_msg) from exc
        return comic

    @classmethod
    def _get_date_interval(
        cls,
        from_date: dt.date | str | None,
        to_date: dt.date | str | None,
    ) -> tuple[dt.date | None, dt.date | None]:
        if isinstance(from_date, str):
            from_date = dt.datetime.strptime(from_date, cls.DATE_FORMAT).date()
        logger.debug("From date: %s", from_date)

        if isinstance(to_date, str):
            to_date = dt.datetime.strptime(to_date, cls.DATE_FORMAT).date()
        logger.debug("To date: %s", to_date)

        if from_date and to_date and from_date > to_date:
            error_msg = f"From date ({from_date}) after to date ({to_date})"
            logger.error(error_msg)
            raise ComicsError(error_msg)

        return from_date, to_date
