from django.contrib import admin

from comics.core import models


class ReleaseImageInline(admin.TabularInline):
    model = models.Release.images.through
    readonly_fields = ("release", "image")
    extra = 0

    def has_add_permission(self, request):
        return False


@admin.register(models.Comic)
class ComicAdmin(admin.ModelAdmin):
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

    def has_add_permission(self, request):
        return False


@admin.register(models.Release)
class ReleaseAdmin(admin.ModelAdmin):
    list_display = ("__unicode__", "comic", "pub_date", "fetched")
    list_filter = ["pub_date", "fetched", "comic"]
    date_hierarchy = "pub_date"
    exclude = ("images",)
    readonly_fields = ("comic", "pub_date", "fetched")
    inlines = (ReleaseImageInline,)

    def has_add_permission(self, request):
        return False


def text_preview(obj):
    max_length = 60
    if len(obj.text) < max_length:
        return obj.text
    else:
        return obj.text[:max_length] + "..."


@admin.register(models.Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = (
        "__unicode__",
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

    def has_add_permission(self, request):
        return False
