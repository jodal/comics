from __future__ import annotations

import datetime as dt
import logging
from typing import TYPE_CHECKING

from django.db import transaction

from comics.core.exceptions import MetadataError
from comics.core.files import sha256sum
from comics.core.models import Comic, Image, Release

if TYPE_CHECKING:
    from collections.abc import Sequence

    from django.core.files import File

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
            slug=metadata.slug,
            defaults={
                "language": metadata.language,
                "name": metadata.name,
                "url": metadata.url,
                "active": metadata.active,
                "start_date": _parse_optional_date(metadata, "start_date"),
                "end_date": _parse_optional_date(metadata, "end_date"),
                "rights": metadata.rights,
            },
        )
        return comic


class ReleaseService:
    @staticmethod
    @transaction.atomic
    def create(
        *,
        comic: Comic,
        pub_date: dt.date,
        images: Sequence[Image],
    ) -> Release:
        """Store a release of the comic, made up of the given images."""
        release = Release(comic=comic, pub_date=pub_date)
        release.save()
        release.images.add(*images)
        return release


class ImageService:
    @staticmethod
    @transaction.atomic
    def create(
        *,
        comic: Comic,
        file: File,
        file_extension: str,
        title: str | None = None,
        text: str | None = None,
    ) -> Image:
        """Store an image of the comic, named after the checksum of its contents.

        The file must have a name of its own, which is not the name it is
        stored under: Django reads the image's dimensions off the file it
        is given, and silently reads nothing from a nameless one.
        """
        if not file_extension:
            msg = "The file extension must be non-empty"
            raise ValueError(msg)

        checksum = sha256sum(file)
        image = Image(comic=comic, checksum=checksum)
        image.file.save(f"{checksum}{file_extension}", file)
        if title is not None:
            image.title = title
        if text is not None:
            image.text = text
        image.save()
        return image
