from django.contrib import admin

from comics.sets import models


@admin.register(models.Set)
class SetAdmin(admin.ModelAdmin):
    list_display = ('name', 'created', 'last_modified', 'last_loaded')
