from django.contrib import admin

from comics.core import models

class ComicAdmin(admin.ModelAdmin):
    list_display = ('name', 'language', 'slug', 'url', 'rights')
    prepopulated_fields = {
        'slug': ('name',)
    }

class ReleaseAdmin(admin.ModelAdmin):
    list_display = ('comic', 'pub_date', 'fetched')
    list_filter = ['pub_date', 'fetched', 'comic']
    date_hierarchy = 'pub_date'

class ImageAdmin(admin.ModelAdmin):
    list_display = ('file', 'height', 'width', 'fetched', 'title', 'text')
    list_filter = ['fetched', 'comic']
    date_hierarchy = 'fetched'

admin.site.register(models.Comic, ComicAdmin)
admin.site.register(models.Release, ReleaseAdmin)
admin.site.register(models.Image, ImageAdmin)
