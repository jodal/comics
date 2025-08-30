import datetime as dt
from unittest.mock import Mock

import pytest
from pytest_mock import MockerFixture

from comics.aggregator.command import Aggregator, AggregatorConfig
from comics.aggregator.crawler import CrawlerBase, CrawlerRelease
from comics.aggregator.downloader import ReleaseDownloader
from comics.core.models import Comic


@pytest.fixture
def aggregator(comics: list[Comic]) -> Aggregator:
    config = AggregatorConfig()
    aggregator = Aggregator(config)
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


def test_init_options(aggregator: Aggregator) -> None:
    result = Aggregator(
        options={
            "comics_slugs": None,
            "from_date": None,
            "to_date": None,
        }
    )

    assert len(aggregator.config.comics) == len(result.config.comics)
    assert aggregator.config.from_date == result.config.from_date
    assert aggregator.config.to_date == result.config.to_date


def test_crawl_one_comic_one_date(
    aggregator: Aggregator,
    comic_mock: Mock,
    crawler_mock: Mock,
) -> None:
    pub_date = dt.date(2008, 3, 1)
    crawler_release = CrawlerRelease(comic_mock, pub_date)
    crawler_mock.get_crawler_release.return_value = crawler_release

    aggregator._crawl_one_comic_one_date(crawler_mock, pub_date)  # pyright: ignore[reportPrivateUsage]

    assert crawler_mock.get_crawler_release.call_count == 1
    crawler_mock.get_crawler_release.assert_called_with(pub_date)


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


def test_get_valid_date_from_history_capable(
    aggregator: Aggregator,
    crawler_mock: Mock,
) -> None:
    expected = dt.date(2008, 3, 1)
    crawler_mock.comic = Comic.objects.get(slug="xkcd")
    crawler_mock.history_capable = expected
    crawler_mock.current_date = dt.date(2008, 4, 1)

    result = aggregator._get_valid_date(crawler_mock, dt.date(2008, 2, 1))  # pyright: ignore[reportPrivateUsage]

    assert result == expected


def test_get_valid_date_from_config(
    aggregator: Aggregator,
    crawler_mock: Mock,
) -> None:
    expected = dt.date(2008, 3, 1)
    crawler_mock.comic = Comic.objects.get(slug="xkcd")
    crawler_mock.history_capable = dt.date(2008, 1, 1)
    crawler_mock.current_date = dt.date(2008, 4, 1)

    result = aggregator._get_valid_date(crawler_mock, expected)  # pyright: ignore[reportPrivateUsage]

    assert result == expected


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
