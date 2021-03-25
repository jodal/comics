import json

from django.test import TestCase
from django.test.client import Client

from comics.accounts.models import Subscription
from comics.core.models import Comic

from . import create_subscriptions, create_user


class SubscriptionsResourceTestCase(TestCase):
    fixtures = ["comics.json"]

    def setUp(self):
        self.user = create_user()
        create_subscriptions(self.user)
        self.client = Client()

    def test_requires_authentication(self):
        response = self.client.get("/api/v1/subscriptions/")

        self.assertEqual(response.status_code, 401)

    def test_authentication_with_secret_key_in_header(self):
        response = self.client.get(
            "/api/v1/subscriptions/", HTTP_AUTHORIZATION="Key s3cretk3y"
        )

        self.assertEqual(response.status_code, 200)

    def test_list_subscriptions(self):
        subscription = Subscription.objects.all()[0]

        response = self.client.get(
            "/api/v1/subscriptions/", HTTP_AUTHORIZATION="Key s3cretk3y"
        )

        data = json.loads(response.content)
        self.assertEqual(len(data["objects"]), 2)

        sub = data["objects"][0]
        self.assertEqual(
            sub["resource_uri"], "/api/v1/subscriptions/%d/" % subscription.pk
        )
        self.assertEqual(sub["comic"], "/api/v1/comics/%d/" % subscription.comic.pk)

    def test_comic_filter(self):
        subscription = Subscription.objects.get(comic__slug="xkcd")

        response = self.client.get(
            "/api/v1/subscriptions/",
            {"comic__slug": "xkcd"},
            HTTP_AUTHORIZATION="Key s3cretk3y",
        )

        data = json.loads(response.content)
        self.assertEqual(len(data["objects"]), 1)

        sub = data["objects"][0]
        self.assertEqual(
            sub["resource_uri"], "/api/v1/subscriptions/%d/" % subscription.pk
        )
        self.assertEqual(sub["comic"], "/api/v1/comics/9/")

    def test_details_view(self):
        subscription = Subscription.objects.all()[0]

        response = self.client.get(
            "/api/v1/subscriptions/", HTTP_AUTHORIZATION="Key s3cretk3y"
        )

        data = json.loads(response.content)
        sub = data["objects"][0]
        self.assertEqual(
            sub["resource_uri"], "/api/v1/subscriptions/%d/" % subscription.pk
        )

        response = self.client.get(
            sub["resource_uri"], HTTP_AUTHORIZATION="Key s3cretk3y"
        )

        data = json.loads(response.content)
        self.assertEqual(data["comic"], "/api/v1/comics/%d/" % subscription.comic.pk)

    def test_subscribe_to_comic(self):
        comic = Comic.objects.get(slug="bunny")

        data = json.dumps({"comic": "/api/v1/comics/%d/" % comic.pk})
        response = self.client.post(
            "/api/v1/subscriptions/",
            data=data,
            content_type="application/json",
            HTTP_AUTHORIZATION="Key s3cretk3y",
        )

        self.assertEqual(response.status_code, 201)

        subscription = Subscription.objects.get(
            userprofile__user=self.user, comic=comic
        )
        self.assertEqual(
            response["Location"], "/api/v1/subscriptions/%d/" % subscription.pk
        )

        self.assertEqual(response.content, b"")

    def test_unsubscribe_from_comic(self):
        sub = Subscription.objects.get(comic__slug="xkcd")

        self.assertEqual(
            2, Subscription.objects.filter(userprofile__user=self.user).count()
        )

        response = self.client.delete(
            "/api/v1/subscriptions/%d/" % sub.pk,
            HTTP_AUTHORIZATION="Key s3cretk3y",
        )

        self.assertEqual(response.status_code, 204)
        self.assertEqual(response.content, b"")

        self.assertEqual(
            1, Subscription.objects.filter(userprofile__user=self.user).count()
        )

    def test_bulk_update(self):
        # XXX: "PATCH /api/v1/subscriptions/" isn't tested as Django's test
        # client doesn't support the PATCH method yet. See
        # https://code.djangoproject.com/ticket/17797 to check if PATCH support
        # has been added yet.
        pass
