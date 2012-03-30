from django.contrib import admin

from comics.sets import models


class SetAdmin(admin.ModelAdmin):
    list_display = ('name', 'created', 'last_modified', 'last_loaded')


class UserSetAdmin(admin.ModelAdmin):
    list_display = ('user',)


admin.site.register(models.Set, SetAdmin)
admin.site.register(models.UserSet, UserSetAdmin)
