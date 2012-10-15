from django.contrib import admin

from comics.core import models


class ComicAdmin(admin.ModelAdmin):
    list_display = ('slug', 'name', 'language', 'url', 'rights', 'start_date',
        'end_date', 'active')
    prepopulated_fields = {
        'slug': ('name',)
    }
    list_filter = ['active', 'language']


class ReleaseAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'comic', 'pub_date', 'fetched')
    list_filter = ['pub_date', 'fetched', 'comic']
    date_hierarchy = 'pub_date'
    exclude = ('images',)


class ImageAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'file', 'height', 'width', 'fetched', 'title', 'text')
    list_filter = ['fetched', 'comic']
    date_hierarchy = 'fetched'


admin.site.register(models.Comic, ComicAdmin)
admin.site.register(models.Release, ReleaseAdmin)
admin.site.register(models.Image, ImageAdmin)
