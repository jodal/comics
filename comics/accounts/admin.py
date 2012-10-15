from django.contrib import admin

from comics.accounts import models


class SubscriptionInline(admin.StackedInline):
    model = models.Subscription
    extra = 1


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'secret_key')
    inlines = [SubscriptionInline,]


admin.site.register(models.UserProfile, UserProfileAdmin)
