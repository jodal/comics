from django.contrib.auth.models import User

from comics.accounts.models import Subscription
from comics.core.models import Comic


def create_user():
    user = User.objects.create_user("alice", "alice@example.com", "secret")
    user.comics_profile.secret_key = "s3cretk3y"
    user.comics_profile.save()
    return user


def create_subscriptions(user):
    Subscription.objects.create(
        userprofile=user.comics_profile,
        comic=Comic.objects.get(slug="geekandpoke"),
    )
    Subscription.objects.create(
        userprofile=user.comics_profile, comic=Comic.objects.get(slug="xkcd")
    )
