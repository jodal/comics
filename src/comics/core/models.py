from __future__ import annotations

import datetime as dt
import os

from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django_stubs_ext.db.models import TypedModelMeta

from comics.core.enums import Language
from comics.core.managers import ComicManager


class Comic(models.Model):
    # Required fields
    name = models.CharField[str, str](
        max_length=100,
        help_text="Name of the comic",
    )
    slug = models.SlugField[str, str](
        max_length=100,
        unique=True,
        verbose_name="Short name",
        help_text="For file paths and URLs",
    )
    language = models.CharField[str, str](
        max_length=2,
        choices=Language.choices,
        help_text="The language of the comic",
    )

    # Optional fields
    url = models.URLField[str, str](
        verbose_name="URL",
        blank=True,
        help_text="URL to the official website",
    )
    active = models.BooleanField[bool, bool](
        default=True,
        help_text="Wheter the comic is still being crawled",
    )
    start_date = models.DateField[dt.date | None, dt.date | None](
        blank=True,
        null=True,
        help_text="First published at",
    )
    end_date = models.DateField[dt.date | None, dt.date | None](
        blank=True,
        null=True,
        help_text="Last published at, if comic has been cancelled",
    )
    rights = models.CharField[str, str](
        max_length=100,
        blank=True,
        help_text="Author, copyright, and/or licensing information",
    )

    # Automatically populated fields
    added = models.DateTimeField[dt.datetime, dt.datetime](
        auto_now_add=True,
        help_text="Time the comic was added to the site",
    )

    objects = ComicManager()

    class Meta(TypedModelMeta):
        db_table = "comics_comic"
        ordering = ["name"]

    def __str__(self) -> str:
        return self.slug

    def get_absolute_url(self) -> str:
        return reverse("comic_latest", kwargs={"comic_slug": self.slug})

    def get_redirect_url(self) -> str:
        return reverse("comic_website", kwargs={"comic_slug": self.slug})

    def is_new(self) -> bool:
        some_time_ago = timezone.now() - dt.timedelta(
            days=settings.COMICS_NUM_DAYS_COMIC_IS_NEW
        )
        return self.added > some_time_ago


class Release(models.Model):
    # Required fields
    comic = models.ForeignKey["Release", "Comic"](
        Comic,
        on_delete=models.CASCADE,
    )
    pub_date = models.DateField[dt.date, dt.date](
        verbose_name="publication date",
        db_index=True,
    )
    images = models.ManyToManyField["Image", "Release"](
        "Image",
        related_name="releases",
    )

    # Automatically populated fields
    fetched = models.DateTimeField[dt.datetime, dt.datetime](
        auto_now_add=True,
        db_index=True,
    )

    class Meta(TypedModelMeta):
        db_table = "comics_release"
        indexes = [models.Index(fields=["comic", "pub_date"])]
        get_latest_by = "pub_date"

    def __str__(self) -> str:
        return f"Release {self.comic.slug}/{self.pub_date}"

    def get_absolute_url(self) -> str:
        return reverse(
            "comic_day",
            kwargs={
                "comic_slug": self.comic.slug,
                "year": self.pub_date.year,
                "month": self.pub_date.month,
                "day": self.pub_date.day,
            },
        )

    def get_ordered_images(self) -> list[Image]:
        if not getattr(self, "_ordered_images", []):
            self._ordered_images = list(self.images.order_by("id"))
        return self._ordered_images


# Let all created dirs and files be writable by the group
os.umask(0o002)

image_storage = FileSystemStorage(
    location=settings.MEDIA_ROOT,
    base_url=settings.MEDIA_URL,
)


def image_file_path(instance: Image, filename: str) -> str:
    return f"{instance.comic.slug}/{filename[0]}/{filename}"


class Image(models.Model):
    # Required fields
    comic = models.ForeignKey["Image", "Comic"](
        Comic,
        on_delete=models.CASCADE,
    )
    file = models.ImageField(
        storage=image_storage,
        upload_to=image_file_path,
        height_field="height",
        width_field="width",
    )
    checksum = models.CharField[str, str](
        max_length=64,
        db_index=True,
    )

    # Optional fields
    title = models.CharField[str, str](
        max_length=255,
        blank=True,
    )
    text = models.TextField[str, str](
        blank=True,
    )

    # Automatically populated fields
    fetched = models.DateTimeField[dt.datetime, dt.datetime](
        auto_now_add=True,
    )
    height = models.IntegerField[int, int]()
    width = models.IntegerField[int, int]()

    class Meta(TypedModelMeta):
        db_table = "comics_image"

    def __str__(self) -> str:
        return f"Image {self.comic.slug}/{self.checksum[:8]}..."
