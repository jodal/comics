from django.contrib import admin

from comics.accounts import models


class SubscriptionInline(admin.StackedInline):
    model = models.Subscription
    extra = 1


def email(obj):
    return obj.user.email


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', email, 'secret_key')
    inlines = [SubscriptionInline,]
    readonly_fields = ('user',)


admin.site.register(models.UserProfile, UserProfileAdmin)
