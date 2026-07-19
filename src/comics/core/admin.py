from __future__ import annotations

from typing import TYPE_CHECKING

from django.contrib import admin

from comics.core import models

if TYPE_CHECKING:
    from django.db.models import Model
    from django.http import HttpRequest


class ReleaseImageInline(admin.TabularInline["Model", "Model"]):
    model = models.Release.images.through
    readonly_fields = ("release", "image")
    extra = 0

    def has_add_permission(
        self,
        request: HttpRequest,
        obj: Model | None = None,
    ) -> bool:
        return False


@admin.register(models.Comic)
class ComicAdmin(admin.ModelAdmin[models.Comic]):
    list_display = (
        "slug",
        "name",
        "language",
        "url",
        "rights",
        "start_date",
        "end_date",
        "active",
    )
    list_filter = ["active", "language"]
    readonly_fields = (
        "name",
        "slug",
        "language",
        "url",
        "rights",
        "start_date",
        "end_date",
        "active",
    )

    def has_add_permission(self, request: HttpRequest) -> bool:
        return False


@admin.register(models.Release)
class ReleaseAdmin(admin.ModelAdmin[models.Release]):
    list_display = ("__str__", "comic", "pub_date", "fetched")
    list_filter = ["pub_date", "fetched", "comic"]
    date_hierarchy = "pub_date"
    exclude = ("images",)
    readonly_fields = ("comic", "pub_date", "fetched")
    inlines = (ReleaseImageInline,)

    def has_add_permission(self, request: HttpRequest) -> bool:
        return False


def text_preview(obj: models.Image) -> str:
    max_length = 60
    if len(obj.text) < max_length:
        return obj.text
    else:
        return obj.text[:max_length] + "..."


@admin.register(models.Image)
class ImageAdmin(admin.ModelAdmin[models.Image]):
    list_display = (
        "__str__",
        "file",
        "height",
        "width",
        "fetched",
        "title",
        text_preview,
    )
    list_editable = ("title",)
    list_filter = ["fetched", "comic"]
    date_hierarchy = "fetched"
    readonly_fields = (
        "comic",
        "file",
        "checksum",
        "height",
        "width",
        "fetched",
    )
    inlines = (ReleaseImageInline,)

    def has_add_permission(self, request: HttpRequest) -> bool:
        return False
