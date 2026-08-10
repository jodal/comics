import datetime as dt
import logging
from dataclasses import dataclass, field

from comics.comics import get_comic_module, get_comic_module_names
from comics.core.exceptions import MetadataError
from comics.core.models import Comic

logger = logging.getLogger("comics.core.metadata")


@dataclass
class MetadataBase:
    """Base class for the metadata part of a crawler module.

    Each crawler module must define a subclass of this class named
    `Metadata`, overriding the class attributes to describe the comic. The
    metadata is used for display at the web site.
    """

    language: str = field(init=False)
    """*Required.* A two-letter string with the language code for the language
    used in the comic. Typically `"en"` or `"no"`.

    The language code must also be present in
    `comics.core.models.Comic.LANGUAGES`.
    """

    slug: str = field(init=False)
    """The comic's slug, used in URLs and to identify the comic.

    Set automatically to the crawler module's file name, so it cannot be
    overridden.
    """

    name: str = field(init=False)
    """*Required.* A string with the name of the comic."""

    url: str = field(init=False)
    """*Required.* A string with the URL of the comic's web page."""

    active: bool = field(init=False, default=True)
    """*Optional.* Whether or not this comic is still being crawled.

    Defaults to `True`.
    """

    start_date: str | None = field(init=False, default=None)
    """*Optional.* The first date the comic was published at, as an
    ISO 8601 date string, e.g. `"2005-05-29"`."""

    end_date: str | None = field(init=False, default=None)
    """*Optional.* The last date the comic was published at, as an ISO 8601
    date string, if the comic is discontinued."""

    rights: str = field(init=False, default="")
    """*Optional.* Name of the author and the comic's license if available."""

    def __post_init__(self) -> None:
        self.slug = self.__module__.split(".")[-1]


def get_metadata(comic_slug: str) -> MetadataBase | None:
    """The metadata a comic module describes itself with.

    Returns `None` if the module cannot be imported or does not describe a
    comic, after logging why. Reading metadata must never fail for the whole
    run just because a single comic module is broken.
    """
    logger.debug("Importing comic module for %s", comic_slug)
    try:
        comic_module = get_comic_module(comic_slug)
    except Exception:
        logger.exception("%s: Could not import the comic module", comic_slug)
        return None

    metadata_class = getattr(comic_module, "Metadata", None)
    if metadata_class is None:
        logger.error("%s: Comic module has no Metadata class", comic_slug)
        return None

    try:
        metadata = metadata_class()
    except Exception:
        logger.exception("%s: Could not read the comic's metadata", comic_slug)
        return None

    if not isinstance(metadata, MetadataBase):
        logger.error("%s: Metadata is not a MetadataBase subclass", comic_slug)
        return None

    return metadata


def select_comic_slugs(requested: list[str]) -> list[str]:
    """The comic slugs to load metadata for.

    An explicitly named comic is always selected, active or not. With
    `"all"`, a comic is only selected if it is still active or already in
    the database, so a new installation is not seeded with comics it has
    never served.
    """
    if len(requested) == 0:
        return []

    if "all" not in requested:
        logger.debug("Load targets: %s", requested)
        return requested

    known_slugs = set(Comic.objects.values_list("slug", flat=True))
    selected = [
        comic_slug
        for comic_slug in get_comic_module_names()
        if comic_slug in known_slugs
        or ((metadata := get_metadata(comic_slug)) is not None and metadata.active)
    ]
    logger.debug("Load targets: all comics (%d of them)", len(selected))
    return selected


def load_metadata(comic_slugs: list[str]) -> None:
    """Update the database with the metadata the given comics describe."""
    for comic_slug in comic_slugs:
        logger.info("Loading metadata for %s", comic_slug)
        metadata = get_metadata(comic_slug)
        if metadata is None:
            return

        try:
            _update_comic(metadata)
        except MetadataError as error:
            logger.error("%s: %s", comic_slug, error)
        except Exception:
            logger.exception("%s: Could not update the comic", comic_slug)


def _parse_optional_date(metadata: MetadataBase, field_name: str) -> dt.date | None:
    value: str | None = getattr(metadata, field_name)
    if value is None:
        return None
    try:
        return dt.date.fromisoformat(value)
    except ValueError as error:
        msg = f"Invalid {field_name}: {value!r}. Expected YYYY-MM-DD."
        raise MetadataError(msg) from error


def _update_comic(metadata: MetadataBase) -> None:
    """Update the comic in the database to match its metadata.

    Raises `MetadataError` if the metadata does not describe a valid comic.
    """
    logger.debug("Updating database with: %s", metadata)
    Comic.objects.update_or_create(
        language=metadata.language,
        slug=metadata.slug,
        defaults={
            "name": metadata.name,
            "url": metadata.url,
            "active": metadata.active,
            "start_date": _parse_optional_date(metadata, "start_date"),
            "end_date": _parse_optional_date(metadata, "end_date"),
            "rights": metadata.rights,
        },
    )
