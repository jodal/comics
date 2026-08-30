import datetime as dt
import logging
from unittest.mock import Mock

import pytest
from pytest_mock import MockerFixture

from comics.aggregator import command
from comics.aggregator.command import Aggregator
from comics.aggregator.crawler import CrawlerBase, CrawlerRelease
from comics.aggregator.downloader import ReleaseDownloader
from comics.aggregator.exceptions import (
    CrawlerHTTPError,
    ImageURLNotFound,
    ReleaseAlreadyExists,
)
from comics.core.models import Comic


@pytest.fixture
def aggregator(comics: list[Comic]) -> Aggregator:
    aggregator = Aggregator(comics)
    aggregator.identifier = "slug"
    return aggregator


@pytest.fixture
def comic_mock(mocker: MockerFixture) -> Mock:
    comic = mocker.Mock(spec=Comic)
    comic.slug = "slug"
    return comic


@pytest.fixture
def crawler_mock(mocker: MockerFixture, comic_mock: Mock) -> Mock:
    crawler = mocker.Mock(spec=CrawlerBase)
    crawler.comic = comic_mock
    return crawler


@pytest.fixture
def downloader_mock(mocker: MockerFixture) -> Mock:
    return mocker.Mock(spec=ReleaseDownloader)


def test_crawl_one_comic_one_date(
    aggregator: Aggregator,
    comic_mock: Mock,
    crawler_mock: Mock,
) -> None:
    pub_date = dt.date(2008, 3, 1)
    crawler_release = CrawlerRelease(comic_mock, pub_date)
    crawler_mock.get_release.return_value = crawler_release

    aggregator._crawl_one_comic_one_date(crawler_mock, pub_date)  # pyright: ignore[reportPrivateUsage]

    assert crawler_mock.get_release.call_count == 1
    crawler_mock.get_release.assert_called_with(pub_date)


def test_download_release(
    aggregator: Aggregator,
    comic_mock: Mock,
    downloader_mock: Mock,
) -> None:
    crawler_release = CrawlerRelease(comic_mock, dt.date(2008, 3, 1))
    aggregator._get_downloader = lambda: downloader_mock  # pyright: ignore[reportPrivateUsage]

    aggregator._download_release(crawler_release)  # pyright: ignore[reportPrivateUsage]

    assert downloader_mock.download.call_count == 1
    downloader_mock.download.assert_called_with(crawler_release)


def test_get_valid_date_from_history_start(
    aggregator: Aggregator,
    crawler_mock: Mock,
) -> None:
    expected = dt.date(2008, 3, 1)
    crawler_mock.comic = Comic.objects.get(slug="xkcd")
    crawler_mock.history_start = expected
    crawler_mock.current_date = dt.date(2008, 4, 1)

    result = aggregator._get_valid_date(crawler_mock, dt.date(2008, 2, 1))  # pyright: ignore[reportPrivateUsage]

    assert result == expected


def test_get_valid_date_from_config(
    aggregator: Aggregator,
    crawler_mock: Mock,
) -> None:
    expected = dt.date(2008, 3, 1)
    crawler_mock.comic = Comic.objects.get(slug="xkcd")
    crawler_mock.history_start = dt.date(2008, 1, 1)
    crawler_mock.current_date = dt.date(2008, 4, 1)

    result = aggregator._get_valid_date(crawler_mock, expected)  # pyright: ignore[reportPrivateUsage]

    assert result == expected


@pytest.mark.parametrize(
    ("error", "expected_level"),
    [
        (
            ReleaseAlreadyExists(slug="xkcd", pub_date=dt.date(2008, 3, 1)),
            logging.INFO,
        ),
        (
            CrawlerHTTPError(slug="xkcd", pub_date=dt.date(2008, 3, 1)),
            logging.WARNING,
        ),
        (
            ImageURLNotFound(slug="xkcd", pub_date=dt.date(2008, 3, 1)),
            logging.ERROR,
        ),
    ],
)
def test_crawl_logs_error_at_level_matching_its_category(
    aggregator: Aggregator,
    crawler_mock: Mock,
    caplog: pytest.LogCaptureFixture,
    error: Exception,
    expected_level: int,
) -> None:
    crawler_mock.get_release.side_effect = error

    with caplog.at_level(logging.INFO):
        result = aggregator._crawl_one_comic_one_date(  # pyright: ignore[reportPrivateUsage]
            crawler_mock, dt.date(2008, 3, 1)
        )

    assert result is None
    assert [record.levelno for record in caplog.records] == [expected_level]


def test_crawl_fingerprints_broken_crawler_per_comic_and_cause(
    aggregator: Aggregator,
    crawler_mock: Mock,
    mocker: MockerFixture,
) -> None:
    scope = mocker.MagicMock()
    mocker.patch.object(
        command.sentry_sdk, "new_scope"
    ).return_value.__enter__.return_value = scope
    crawler_mock.get_release.side_effect = ImageURLNotFound(
        slug="xkcd", pub_date=dt.date(2008, 3, 1)
    )

    aggregator._crawl_one_comic_one_date(  # pyright: ignore[reportPrivateUsage]
        crawler_mock, dt.date(2008, 3, 1)
    )

    assert scope.fingerprint == ["crawler-broken", "xkcd", "ImageURLNotFound"]
    scope.set_tag.assert_called_once_with("comic", "xkcd")


@pytest.mark.skip
def test_get_crawler() -> None:
    pass  # TODO


@pytest.mark.skip
def test_get_downloader() -> None:
    pass  # TODO


@pytest.mark.skip
def test_aggregate_one_comic() -> None:
    pass  # TODO


@pytest.mark.skip
def test_start() -> None:
    pass  # TODO
