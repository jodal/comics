from __future__ import annotations

import datetime as dt
import logging
from typing import TYPE_CHECKING

from comics.core.exceptions import MetadataError
from comics.core.models import Comic

if TYPE_CHECKING:
    from comics.core.metadata import MetadataBase

logger = logging.getLogger("comics.core.services")


def _parse_optional_date(metadata: MetadataBase, field_name: str) -> dt.date | None:
    value: str | None = getattr(metadata, field_name)
    if value is None:
        return None
    try:
        return dt.date.fromisoformat(value)
    except ValueError as error:
        msg = f"Invalid {field_name}: {value!r}. Expected YYYY-MM-DD."
        raise MetadataError(msg) from error


class ComicService:
    @staticmethod
    def create_or_update(*, metadata: MetadataBase) -> Comic:
        """Make the comic in the database match its metadata.

        Raises `MetadataError` if the metadata does not describe a valid
        comic.
        """
        logger.debug("Updating database with: %s", metadata)
        comic, _ = Comic.objects.update_or_create(
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
        return comic
