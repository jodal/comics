from django.contrib import admin

from comics.sets import models

class NamedSetAdmin(admin.ModelAdmin):
    list_display = ('name', 'created', 'last_modified', 'last_loaded')

class UserSetAdmin(admin.ModelAdmin):
    list_display = ('user', 'last_modified', 'last_loaded')

admin.site.register(models.NamedSet, NamedSetAdmin)
admin.site.register(models.UserSet, UserSetAdmin)
