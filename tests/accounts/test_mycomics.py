import pytest
from django.contrib.auth.models import User
from django.contrib.messages import get_messages
from django.test.client import Client
from django.urls import reverse

from comics.accounts.models import Subscription
from comics.core.models import Comic


@pytest.fixture
def comic(db: None) -> Comic:
    return Comic.objects.create(name="xkcd", slug="xkcd", language="en")


def test_adding_a_comic_twice_is_idempotent(
    db: None,
    client: Client,
    user: User,
    comic: Comic,
) -> None:
    client.force_login(user)

    for _ in range(2):
        response = client.post(
            reverse("toggle_comic"),
            {"comic": comic.slug, "add_comic": "1"},
        )
        assert response.status_code == 302

    assert Subscription.objects.filter(userprofile__user=user, comic=comic).count() == 1


def test_removing_a_comic_twice_is_idempotent(
    db: None,
    client: Client,
    user: User,
    comic: Comic,
) -> None:
    client.force_login(user)
    Subscription.objects.create(userprofile=user.comics_profile, comic=comic)

    for _ in range(2):
        response = client.post(
            reverse("toggle_comic"),
            {"comic": comic.slug, "remove_comic": "1"},
        )
        assert response.status_code == 302

    assert not Subscription.objects.filter(userprofile__user=user).exists()


def test_editing_comics_replaces_the_subscriptions(
    db: None,
    client: Client,
    user: User,
    comic: Comic,
) -> None:
    other = Comic.objects.create(name="Bunny", slug="bunny", language="en")
    kept = Comic.objects.create(name="Nemi", slug="nemi", language="no")
    for subscribed_to in (comic, kept):
        Subscription.objects.create(
            userprofile=user.comics_profile, comic=subscribed_to
        )
    client.force_login(user)

    response = client.post(reverse("edit_comics"), {other.slug: "1", kept.slug: "1"})

    assert response.status_code == 302
    assert set(Comic.objects.subscribed_by(user)) == {other, kept}

    reported = [str(message) for message in get_messages(response.wsgi_request)]
    assert reported == [
        'Removed "xkcd" from my comics',
        'Added "Bunny" to my comics',
    ]


def test_editing_comics_with_nothing_selected_unsubscribes_from_everything(
    db: None,
    client: Client,
    user: User,
    comic: Comic,
) -> None:
    Subscription.objects.create(userprofile=user.comics_profile, comic=comic)
    client.force_login(user)

    response = client.post(reverse("edit_comics"), {})

    assert response.status_code == 302
    assert not Comic.objects.subscribed_by(user).exists()
