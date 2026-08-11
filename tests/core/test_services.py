from __future__ import annotations

import datetime as dt

import pytest

from comics.core.exceptions import MetadataError
from comics.core.metadata import MetadataBase
from comics.core.models import Comic
from comics.core.services import ComicService

# A slug of its own, as other tests may have loaded comics into the database.
SLUG = "examplecomic"


def make_metadata(
    *,
    slug: str = SLUG,
    name: str = "Example Comic",
    language: str = "en",
    url: str = "https://example.com/",
    active: bool = True,
    start_date: str | None = None,
    end_date: str | None = None,
    rights: str = "",
) -> MetadataBase:
    """Metadata as a comic module would declare it.

    The fields are assigned rather than passed to the constructor because
    a comic module declares them as class attributes, and because
    `MetadataBase` derives the slug from the module it is declared in.
    """
    metadata = MetadataBase()
    metadata.slug = slug
    metadata.name = name
    metadata.language = language
    metadata.url = url
    metadata.active = active
    metadata.start_date = start_date
    metadata.end_date = end_date
    metadata.rights = rights
    return metadata


def test_creates_a_comic(db: None) -> None:
    metadata = make_metadata(start_date="2005-05-29", rights="Randall Munroe")

    comic = ComicService.create_or_update(metadata=metadata)

    assert comic.slug == SLUG
    assert comic.name == "Example Comic"
    assert comic.language == "en"
    assert comic.url == "https://example.com/"
    assert comic.active is True
    assert comic.start_date == dt.date(2005, 5, 29)
    assert comic.end_date is None
    assert comic.rights == "Randall Munroe"


def test_updates_an_existing_comic(db: None) -> None:
    ComicService.create_or_update(metadata=make_metadata())

    comic = ComicService.create_or_update(
        metadata=make_metadata(name="Renamed", active=False, end_date="2026-01-01")
    )

    assert Comic.objects.for_slugs(SLUG).count() == 1
    assert comic.name == "Renamed"
    assert comic.active is False
    assert comic.end_date == dt.date(2026, 1, 1)


@pytest.mark.parametrize(
    ("metadata", "field_name"),
    [
        pytest.param(
            make_metadata(start_date="29.05.2005"), "start_date", id="start_date"
        ),
        pytest.param(make_metadata(end_date="29.05.2005"), "end_date", id="end_date"),
    ],
)
def test_rejects_a_date_that_is_not_iso_8601(
    db: None,
    metadata: MetadataBase,
    field_name: str,
) -> None:
    with pytest.raises(MetadataError, match=field_name):
        ComicService.create_or_update(metadata=metadata)

    assert not Comic.objects.for_slugs(SLUG).exists()
