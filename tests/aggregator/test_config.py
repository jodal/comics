import datetime as dt

import pytest

from comics.aggregator.command import AggregatorConfig
from comics.aggregator.exceptions import ComicsError
from comics.core.models import Comic


def test_config_init() -> None:
    config = AggregatorConfig()
    assert config.comic_slugs == []
    assert config.from_date is None
    assert config.to_date is None


def test_config_with_from_date() -> None:
    config = AggregatorConfig.from_options(from_date=dt.date(2008, 3, 11))
    assert config.from_date == dt.date(2008, 3, 11)


def test_config_with_from_date_from_string() -> None:
    config = AggregatorConfig.from_options(from_date="2008-03-11")
    assert config.from_date == dt.date(2008, 3, 11)


def test_config_with_to_date() -> None:
    config = AggregatorConfig.from_options(to_date=dt.date(2008, 3, 11))
    assert config.to_date == dt.date(2008, 3, 11)


def test_config_with_to_date_from_string() -> None:
    config = AggregatorConfig.from_options(to_date="2008-03-11")
    assert config.to_date == dt.date(2008, 3, 11)


def test_config_validates_dates_valid() -> None:
    AggregatorConfig.from_options(
        from_date=dt.date(2008, 3, 11),
        to_date=dt.date(2008, 3, 11),
    )
    AggregatorConfig.from_options(
        from_date=dt.date(2008, 2, 29),
        to_date=dt.date(2008, 3, 2),
    )


def test_config_validate_dates_invalid() -> None:
    with pytest.raises(ComicsError):
        AggregatorConfig.from_options(
            from_date=dt.date(2008, 3, 11),
            to_date=dt.date(2008, 3, 10),
        )


def test_config_comics_by_slug_valid(comics: list[Comic]) -> None:
    config = AggregatorConfig.from_options(comic_slugs=["xkcd"])
    assert config.comics == [Comic.objects.get(slug="xkcd")]


def test_config_comics_by_slug_invalid(comics: list[Comic]) -> None:
    config = AggregatorConfig.from_options(comic_slugs=["not slug"])
    with pytest.raises(ComicsError):
        config.comics  # noqa: B018


def test_config_all_comics(comics: list[Comic]) -> None:
    config = AggregatorConfig.from_options()
    assert len(config.comic_slugs) == 0
    assert len(config.comics) == 2
    assert set(config.comics) == set(comics)
