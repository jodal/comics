from django.contrib import admin

from comics.accounts import models


class SubscriptionInline(admin.StackedInline):
    model = models.Subscription
    extra = 1


def email(obj):
    return obj.user.email


def subscription_count(obj):
    return obj.comics.count()


@admin.register(models.UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ("user", email, "secret_key", subscription_count)
    inlines = [SubscriptionInline]
    readonly_fields = ("user",)
