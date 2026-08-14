from __future__ import annotations

import datetime as dt
import hashlib
import tempfile
from io import BytesIO
from typing import TYPE_CHECKING

import pytest
from django.core.files import File
from django.core.files.base import ContentFile
from PIL import Image as PILImage

from comics.core.exceptions import MetadataError
from comics.core.files import sha256sum
from comics.core.metadata import MetadataBase
from comics.core.models import Comic, Image
from comics.core.services import ComicService, ImageService, ReleaseService

if TYPE_CHECKING:
    from pathlib import Path

    from pytest_django.fixtures import SettingsWrapper

# A slug of its own, as other tests may have loaded comics into the database.
SLUG = "examplecomic"

PUB_DATE = dt.date(2026, 1, 1)


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


@pytest.fixture
def media_root(settings: SettingsWrapper, tmp_path: Path) -> Path:
    """Keep the saved image files out of the real media directory."""
    settings.MEDIA_ROOT = tmp_path
    return tmp_path


@pytest.fixture
def comic(db: None) -> Comic:
    return Comic.objects.create(name="Example Comic", slug=SLUG, language="en")


def png_bytes(*, width: int = 2, height: int = 3) -> bytes:
    buffer = BytesIO()
    PILImage.new("RGB", (width, height), "red").save(buffer, format="PNG")
    return buffer.getvalue()


def make_png(*, width: int = 2, height: int = 3) -> ContentFile:
    # The file must be named, as Django reads the image dimensions off it.
    return ContentFile(png_bytes(width=width, height=height), name="image.png")


def make_image(comic: Comic, *, width: int = 2, height: int = 3) -> Image:
    return ImageService.create(
        comic=comic,
        file=make_png(width=width, height=height),
        file_extension=".png",
    )


# --- ComicService


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


def test_updates_the_language_of_an_existing_comic(db: None) -> None:
    ComicService.create_or_update(metadata=make_metadata())

    comic = ComicService.create_or_update(metadata=make_metadata(language="no"))

    assert Comic.objects.for_slugs(SLUG).count() == 1
    assert comic.language == "no"


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


# --- ImageService


def test_creates_an_image(db: None, comic: Comic, media_root: Path) -> None:
    contents = png_bytes(width=4, height=5)
    checksum = hashlib.sha256(contents).hexdigest()

    image = ImageService.create(
        comic=comic,
        file=ContentFile(contents, name="image.png"),
        file_extension=".png",
        title="A title",
        text="Some text",
    )

    assert image.comic == comic
    assert image.title == "A title"
    assert image.text == "Some text"
    assert image.width == 4
    assert image.height == 5

    # The checksum is of the file's contents, and names the stored file.
    assert image.checksum == checksum
    assert image.file.name == f"{SLUG}/{checksum[0]}/{checksum}.png"
    assert (media_root / SLUG / checksum[0] / f"{checksum}.png").exists()
    assert (media_root / image.file.name).read_bytes() == contents


@pytest.mark.usefixtures("media_root")
def test_creates_an_image_without_a_title_and_text(db: None, comic: Comic) -> None:
    image = make_image(comic)

    assert image.title == ""
    assert image.text == ""


@pytest.mark.usefixtures("media_root")
def test_creates_an_image_from_a_file_that_has_already_been_read(
    db: None,
    comic: Comic,
) -> None:
    """The downloader hands over a temporary file it has read twice already."""
    contents = png_bytes(width=7, height=11)

    with tempfile.NamedTemporaryFile(suffix="comics") as temp_file:
        temp_file.write(contents)
        temp_file.seek(0)
        file = File(temp_file)

        sha256sum(file)  # As the downloader checksums it,
        PILImage.open(temp_file).load()  # and as it validates it.

        image = ImageService.create(comic=comic, file=file, file_extension=".png")

    assert image.checksum == hashlib.sha256(contents).hexdigest()
    assert image.width == 7
    assert image.height == 11


@pytest.mark.usefixtures("media_root")
def test_refuses_to_store_an_image_without_a_file_extension(
    db: None,
    comic: Comic,
) -> None:
    with pytest.raises(ValueError, match="extension"):
        ImageService.create(comic=comic, file=make_png(), file_extension="")

    assert not Image.objects.for_comics(comic).exists()


# --- ReleaseService


@pytest.mark.usefixtures("media_root")
def test_creates_a_release_with_its_images(db: None, comic: Comic) -> None:
    images = [make_image(comic, width=2), make_image(comic, width=4)]

    release = ReleaseService.create(comic=comic, pub_date=PUB_DATE, images=images)

    assert release.comic == comic
    assert release.pub_date == PUB_DATE
    assert release.ordered_images == images


def test_creates_a_release_without_images(db: None, comic: Comic) -> None:
    release = ReleaseService.create(comic=comic, pub_date=PUB_DATE, images=[])

    assert release.ordered_images == []
