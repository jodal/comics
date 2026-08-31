import datetime as dt

from comics.aggregator.exceptions import ImageIsCorrupt, ImageURLNotFound


def test_identifier_merges_the_comic_and_the_date() -> None:
    error = ImageURLNotFound(slug="xkcd", pub_date=dt.date(2026, 8, 30))

    assert error.identifier == "xkcd/2026-08-30"
    assert str(error) == "xkcd/2026-08-30: Image URL not found"


def test_identifier_includes_the_detail_when_given() -> None:
    error = ImageIsCorrupt(slug="xkcd", pub_date=dt.date(2026, 8, 30), detail="a1b2c3")

    assert error.identifier == "xkcd/2026-08-30/a1b2c3"
