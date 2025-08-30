import datetime as dt
from zoneinfo import ZoneInfo

import pytest
from freezegun import freeze_time
from pytest_mock import MockerFixture

from comics.aggregator import crawler as crawler_mod


@pytest.fixture
def crawler(mocker: MockerFixture) -> crawler_mod.CrawlerBase:
    comic = mocker.Mock()
    return crawler_mod.CrawlerBase(comic)


@pytest.mark.parametrize(
    ("tz_local",),
    [
        ("UTC",),
        ("Europe/Oslo",),
        ("America/New_York",),
    ],
)
def test_current_date_when_crawler_is_in_local_today(
    crawler: crawler_mod.CrawlerBase,
    tz_local: str,
) -> None:
    with freeze_time(dt.datetime(2001, 2, 5, 23, 1, 0, tzinfo=ZoneInfo(tz_local))):
        crawler.time_zone = tz_local
        assert crawler.current_date == dt.date(2001, 2, 5)


@pytest.mark.parametrize(
    ("tz_local", "tz_ahead"),
    [
        ("UTC", "Australia/Sydney"),
        ("Europe/Oslo", "Australia/Sydney"),
        ("America/New_York", "Europe/Moscow"),
    ],
)
def test_current_date_when_crawler_is_in_local_tomorrow(
    crawler: crawler_mod.CrawlerBase,
    tz_local: str,
    tz_ahead: str,
) -> None:
    with freeze_time(dt.datetime(2001, 2, 5, 23, 1, 0, tzinfo=ZoneInfo(tz_local))):
        crawler.time_zone = tz_ahead
        assert crawler.current_date == dt.date(2001, 2, 6)


@pytest.mark.parametrize(
    ("tz_local", "tz_behind"),
    [
        ("UTC", "America/New_York"),
        ("Europe/Oslo", "America/New_York"),
        ("America/New_York", "America/Los_Angeles"),
    ],
)
def test_current_date_when_crawler_is_in_local_yesterday(
    crawler: crawler_mod.CrawlerBase,
    tz_local: str,
    tz_behind: str,
) -> None:
    with freeze_time(dt.datetime(2001, 2, 5, 0, 59, 0, tzinfo=ZoneInfo(tz_local))):
        crawler.time_zone = tz_behind
        assert crawler.current_date == dt.date(2001, 2, 4)
