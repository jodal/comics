import datetime as dt

import pytest

from comics.aggregator.command import parse_date_range, select_comics
from comics.core.exceptions import ComicsError
from comics.core.models import Comic


def test_parse_date_range_without_dates() -> None:
    assert parse_date_range(None, None) == (None, None)


def test_parse_date_range_with_from_date() -> None:
    from_date, _ = parse_date_range(dt.date(2008, 3, 11), None)
    assert from_date == dt.date(2008, 3, 11)


def test_parse_date_range_with_from_date_from_string() -> None:
    from_date, _ = parse_date_range("2008-03-11", None)
    assert from_date == dt.date(2008, 3, 11)


def test_parse_date_range_with_to_date() -> None:
    _, to_date = parse_date_range(None, dt.date(2008, 3, 11))
    assert to_date == dt.date(2008, 3, 11)


def test_parse_date_range_with_to_date_from_string() -> None:
    _, to_date = parse_date_range(None, "2008-03-11")
    assert to_date == dt.date(2008, 3, 11)


def test_parse_date_range_validates_dates_valid() -> None:
    parse_date_range(dt.date(2008, 3, 11), dt.date(2008, 3, 11))
    parse_date_range(dt.date(2008, 2, 29), dt.date(2008, 3, 2))


def test_parse_date_range_validates_dates_invalid() -> None:
    with pytest.raises(ComicsError):
        parse_date_range(dt.date(2008, 3, 11), dt.date(2008, 3, 10))


def test_select_comics_by_slug_valid(comics: list[Comic]) -> None:
    assert select_comics(["xkcd"]) == [Comic.objects.get(slug="xkcd")]


def test_select_comics_by_slug_invalid(comics: list[Comic]) -> None:
    with pytest.raises(ComicsError):
        select_comics(["not slug"])


def test_select_comics_without_slugs_selects_all(comics: list[Comic]) -> None:
    assert set(select_comics([])) == set(comics)


def test_select_comics_with_all_selects_all(comics: list[Comic]) -> None:
    assert set(select_comics(["all"])) == set(comics)
