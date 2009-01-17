from django.contrib import admin

from comics.common import models

class ComicAdmin(admin.ModelAdmin):
    list_display = ('name', 'language', 'slug', 'url', 'time_zone', 'rights')
    prepopulated_fields = {
        'slug': ('name',)
    }

class ReleaseAdmin(admin.ModelAdmin):
    list_display = ('comic', 'pub_date')
    list_filter = ['comic', 'pub_date']
    date_hierarchy = 'pub_date'

class StripAdmin(admin.ModelAdmin):
    list_display = ('comic', 'title', 'fetched')
    list_filter = ['comic', 'fetched']

admin.site.register(models.Comic, ComicAdmin)
admin.site.register(models.Release, ReleaseAdmin)
admin.site.register(models.Strip, StripAdmin)
