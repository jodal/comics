from django.contrib import admin

from comics.common import models

class ComicAdmin(admin.ModelAdmin):
    list_display = ('name', 'language', 'slug', 'url', 'time_zone', 'rights')
    prepopulated_fields = {
        'slug': ('name',)
    }

class StripAdmin(admin.ModelAdmin):
    list_display = ('comic', 'pub_date', 'title', 'fetched')
    list_filter = ['comic', 'pub_date', 'fetched']
    date_hierarchy = 'pub_date'

admin.site.register(models.Comic, ComicAdmin)
admin.site.register(models.Strip, StripAdmin)
