import datetime as dt
import logging
from dataclasses import dataclass, field
from typing import TypedDict

from comics.comics import get_comic_module, get_comic_module_names
from comics.core.exceptions import MetadataError
from comics.core.models import Comic

logger = logging.getLogger("comics.core.metadata")


class Options(TypedDict, total=False):
    comic_slugs: list[str]


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


class MetadataLoader:
    def __init__(self, options: Options) -> None:
        self.include_inactive = self._get_include_inactive(options)
        self.comic_slugs = self._get_comic_slugs(options)

    def start(self) -> None:
        for comic_slug in self.comic_slugs:
            logger.info("Loading metadata for %s", comic_slug)
            self._try_load_metadata(comic_slug)

    def stop(self) -> None:
        pass

    def _get_include_inactive(self, options: Options) -> bool:
        comic_slugs = options.get("comic_slugs", None)
        if comic_slugs is None or len(comic_slugs) == 0:
            logger.debug("Excluding inactive comics")
            return False
        else:
            logger.debug("Including inactive comics")
            return True

    def _get_comic_slugs(self, options: Options) -> list[str]:
        comic_slugs = options.get("comic_slugs", None)
        if comic_slugs is None or len(comic_slugs) == 0:
            logger.error("No comic given. Use -c option to specify comic(s).")
            return []
        elif "all" in comic_slugs:
            logger.debug("Load targets: all comics")
            return get_comic_module_names()
        else:
            logger.debug("Load targets: %s", comic_slugs)
            return comic_slugs

    def _try_load_metadata(self, comic_slug: str) -> None:
        metadata = get_metadata(comic_slug)
        if metadata is None:
            return
        try:
            if self._should_load_metadata(metadata):
                self._load_metadata(metadata)
            else:
                logger.debug("Skipping inactive comic")
        except MetadataError as error:
            logger.error(error)
        except Exception as error:
            logger.exception(error)

    def _should_load_metadata(self, metadata: MetadataBase) -> bool:
        return bool(
            metadata.active
            or self.include_inactive
            or Comic.objects.for_slug(metadata.slug).exists()
        )

    def _load_metadata(self, metadata: MetadataBase) -> None:
        logger.debug("Updating database with: %s", metadata)
        Comic.objects.update_or_create(
            language=metadata.language,
            slug=metadata.slug,
            defaults={
                "name": metadata.name,
                "url": metadata.url,
                "active": metadata.active,
                "start_date": self._parse_optional_date(
                    comic_slug=metadata.slug,
                    field_name="start_date",
                    value=metadata.start_date,
                ),
                "end_date": self._parse_optional_date(
                    comic_slug=metadata.slug,
                    field_name="end_date",
                    value=metadata.end_date,
                ),
                "rights": metadata.rights,
            },
        )

    def _parse_optional_date(
        self,
        comic_slug: str,
        field_name: str,
        value: str | None,
    ) -> dt.date | None:
        if value is None:
            return None
        try:
            return dt.date.fromisoformat(value)
        except ValueError as error:
            msg = (
                f"Invalid {field_name} for comic '{comic_slug}': {value!r}. "
                "Expected YYYY-MM-DD."
            )
            raise MetadataError(msg) from error
