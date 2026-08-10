import json

from django.contrib.auth.models import User
from django.test.client import Client

from comics.accounts.models import Subscription
from comics.core.models import Comic


def test_requires_authentication(db: None, client: Client) -> None:
    response = client.get("/api/v1/subscriptions/")

    assert response.status_code == 401


def test_authentication_with_secret_key_in_header(
    db: None,
    client: Client,
    user: User,
) -> None:
    response = client.get(
        "/api/v1/subscriptions/", headers={"authorization": "Key s3cretk3y"}
    )

    assert response.status_code == 200


def test_list_subscriptions(
    db: None,
    client: Client,
    user: User,
    subscriptions: list[Subscription],
) -> None:
    subscription = Subscription.objects.all()[0]

    response = client.get(
        "/api/v1/subscriptions/", headers={"authorization": "Key s3cretk3y"}
    )

    data = json.loads(response.content)
    assert len(data["objects"]) == 2

    sub = data["objects"][0]
    assert sub["resource_uri"] == f"/api/v1/subscriptions/{subscription.pk}/"
    assert sub["comic"] == f"/api/v1/comics/{subscription.comic.pk}/"


def test_comic_filter(
    db: None,
    client: Client,
    user: User,
    subscriptions: list[Subscription],
) -> None:
    subscription = Subscription.objects.get(comic__slug="xkcd")

    response = client.get(
        "/api/v1/subscriptions/",
        {"comic__slug": "xkcd"},
        headers={"authorization": "Key s3cretk3y"},
    )

    data = json.loads(response.content)
    assert len(data["objects"]) == 1

    sub = data["objects"][0]
    assert sub["resource_uri"] == f"/api/v1/subscriptions/{subscription.pk}/"
    assert sub["comic"] == "/api/v1/comics/9/"


def test_details_view(
    db: None,
    client: Client,
    user: User,
    subscriptions: list[Subscription],
) -> None:
    subscription = Subscription.objects.all()[0]

    response = client.get(
        "/api/v1/subscriptions/", headers={"authorization": "Key s3cretk3y"}
    )

    data = json.loads(response.content)
    sub = data["objects"][0]
    assert sub["resource_uri"] == f"/api/v1/subscriptions/{subscription.pk}/"

    response = client.get(
        sub["resource_uri"], headers={"authorization": "Key s3cretk3y"}
    )

    data = json.loads(response.content)
    assert data["comic"] == f"/api/v1/comics/{subscription.comic.pk}/"


def test_subscribe_to_comic(
    db: None,
    client: Client,
    user: User,
    subscriptions: list[Subscription],
) -> None:
    comic = Comic.objects.get(slug="bunny")

    data = json.dumps({"comic": f"/api/v1/comics/{comic.pk}/"})
    response = client.post(
        "/api/v1/subscriptions/",
        data=data,
        content_type="application/json",
        headers={"authorization": "Key s3cretk3y"},
    )

    assert response.status_code == 201

    subscription = Subscription.objects.get(userprofile__user=user, comic=comic)
    assert response["Location"] == f"/api/v1/subscriptions/{subscription.pk}/"

    assert response.content == b""


def test_subscribe_to_comic_twice_creates_a_duplicate(
    db: None,
    client: Client,
    user: User,
    subscriptions: list[Subscription],
) -> None:
    comic = Comic.objects.get(slug="bunny")

    data = json.dumps({"comic": f"/api/v1/comics/{comic.pk}/"})
    for _ in range(2):
        response = client.post(
            "/api/v1/subscriptions/",
            data=data,
            content_type="application/json",
            headers={"authorization": "Key s3cretk3y"},
        )
        assert response.status_code == 201

    assert Subscription.objects.filter(userprofile__user=user, comic=comic).count() == 2


def test_cannot_change_subscription_comic(
    db: None,
    client: Client,
    user: User,
    subscriptions: list[Subscription],
) -> None:
    """A subscription is subscribed to and unsubscribed from, never repointed."""
    subscription = Subscription.objects.get(comic__slug="xkcd")
    comic = Comic.objects.get(slug="bunny")

    data = json.dumps({"comic": f"/api/v1/comics/{comic.pk}/"})
    response = client.put(
        f"/api/v1/subscriptions/{subscription.pk}/",
        data=data,
        content_type="application/json",
        headers={"authorization": "Key s3cretk3y"},
    )

    assert response.status_code == 405

    subscription.refresh_from_db()
    assert subscription.comic.slug == "xkcd"


def test_unsubscribe_from_comic(
    db: None,
    client: Client,
    user: User,
    subscriptions: list[Subscription],
) -> None:
    sub = Subscription.objects.get(comic__slug="xkcd")

    assert Subscription.objects.filter(userprofile__user=user).count() == 2

    response = client.delete(
        f"/api/v1/subscriptions/{sub.pk}/",
        headers={"authorization": "Key s3cretk3y"},
    )

    assert response.status_code == 204
    assert response.content == b""

    assert Subscription.objects.filter(userprofile__user=user).count() == 1


def test_bulk_update(
    db: None,
    client: Client,
    user: User,
    subscriptions: list[Subscription],
) -> None:
    comic = Comic.objects.get(slug="bunny")
    deleted = subscriptions[0]

    data = json.dumps(
        {
            "objects": [{"comic": f"/api/v1/comics/{comic.pk}/"}],
            "deleted_objects": [f"/api/v1/subscriptions/{deleted.pk}/"],
        }
    )
    response = client.patch(
        "/api/v1/subscriptions/",
        data=data,
        content_type="application/json",
        headers={"authorization": "Key s3cretk3y"},
    )

    assert response.status_code == 202
    assert response.content == b""

    subs = Subscription.objects.filter(userprofile__user=user)
    assert subs.filter(comic=comic).exists()
    assert not subs.filter(pk=deleted.pk).exists()
    assert subs.count() == 2


def test_bulk_update_ignores_resource_uri(
    db: None,
    client: Client,
    user: User,
    subscriptions: list[Subscription],
) -> None:
    """An object is a comic to subscribe to, whether or not it names a subscription."""
    subscription = Subscription.objects.get(comic__slug="xkcd")
    bunny = Comic.objects.get(slug="bunny")
    spikedmath = Comic.objects.get(slug="spikedmath")

    data = json.dumps(
        {
            "objects": [
                {
                    "resource_uri": f"/api/v1/subscriptions/{subscription.pk}/",
                    "comic": f"/api/v1/comics/{bunny.pk}/",
                },
                {
                    "resource_uri": "/api/v1/subscriptions/12345/",
                    "comic": f"/api/v1/comics/{spikedmath.pk}/",
                },
            ]
        }
    )
    response = client.patch(
        "/api/v1/subscriptions/",
        data=data,
        content_type="application/json",
        headers={"authorization": "Key s3cretk3y"},
    )

    assert response.status_code == 202

    subscription.refresh_from_db()
    assert subscription.comic.slug == "xkcd"

    subs = Subscription.objects.filter(userprofile__user=user)
    assert subs.filter(comic=bunny).exists()
    assert subs.filter(comic=spikedmath).exists()
    assert subs.count() == 4


def test_bulk_update_ignores_unknown_deleted_subscription(
    db: None,
    client: Client,
    user: User,
    subscriptions: list[Subscription],
) -> None:
    bob = User.objects.create_user("bob", "bob@example.com", "topsecret")
    bob_sub = Subscription.objects.create(
        userprofile=bob.comics_profile,
        comic=Comic.objects.get(slug="bunny"),
    )

    data = json.dumps(
        {
            "deleted_objects": [
                "/api/v1/subscriptions/12345/",
                f"/api/v1/subscriptions/{bob_sub.pk}/",
            ]
        }
    )
    response = client.patch(
        "/api/v1/subscriptions/",
        data=data,
        content_type="application/json",
        headers={"authorization": "Key s3cretk3y"},
    )

    assert response.status_code == 202
    assert Subscription.objects.filter(pk=bob_sub.pk).exists()
    assert Subscription.objects.filter(userprofile__user=user).count() == 2


def test_bulk_update_rolls_back_on_unknown_comic(
    db: None,
    client: Client,
    user: User,
    subscriptions: list[Subscription],
) -> None:
    comic = Comic.objects.get(slug="bunny")

    data = json.dumps(
        {
            "objects": [
                {"comic": f"/api/v1/comics/{comic.pk}/"},
                {"comic": "/api/v1/comics/12345/"},
            ],
            "deleted_objects": [f"/api/v1/subscriptions/{subscriptions[0].pk}/"],
        }
    )
    response = client.patch(
        "/api/v1/subscriptions/",
        data=data,
        content_type="application/json",
        headers={"authorization": "Key s3cretk3y"},
    )

    assert response.status_code == 400

    subs = Subscription.objects.filter(userprofile__user=user)
    assert not subs.filter(comic=comic).exists()
    assert subs.filter(pk=subscriptions[0].pk).exists()
    assert subs.count() == 2


def test_cannot_read_other_users_subscription(
    db: None,
    client: Client,
    user: User,
    subscriptions: list[Subscription],
) -> None:
    bob = User.objects.create_user("bob", "bob@example.com", "topsecret")
    bob_sub = Subscription.objects.create(
        userprofile=bob.comics_profile,
        comic=Comic.objects.get(slug="bunny"),
    )

    response = client.get(
        f"/api/v1/subscriptions/{bob_sub.pk}/",
        headers={"authorization": "Key s3cretk3y"},
    )

    assert response.status_code == 404


def test_cannot_delete_other_users_subscription(
    db: None,
    client: Client,
    user: User,
    subscriptions: list[Subscription],
) -> None:
    bob = User.objects.create_user("bob", "bob@example.com", "topsecret")
    bob_sub = Subscription.objects.create(
        userprofile=bob.comics_profile,
        comic=Comic.objects.get(slug="bunny"),
    )

    response = client.delete(
        f"/api/v1/subscriptions/{bob_sub.pk}/",
        headers={"authorization": "Key s3cretk3y"},
    )

    assert response.status_code == 404
    assert Subscription.objects.filter(pk=bob_sub.pk).exists()
