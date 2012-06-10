from django.contrib import admin

from comics.accounts import models


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'secret_key')


admin.site.register(models.UserProfile, UserProfileAdmin)
