import datetime as dt
import xml.etree.ElementTree as ET
from typing import TYPE_CHECKING

import pytest
from django.contrib.auth.models import User
from django.test.client import Client

from comics.accounts.models import Subscription
from comics.core.models import Comic, Release

if TYPE_CHECKING:
    from pytest_django.fixtures import SettingsWrapper

    from comics.accounts.models import UserProfile

ATOM = "{http://www.w3.org/2005/Atom}"


@pytest.fixture(autouse=True)
def site_url(settings: "SettingsWrapper") -> None:
    settings.COMICS_SITE_URL = "https://comics.example.com"


def parse_feed(content: bytes) -> ET.Element:
    # Parsing with a strict XML parser proves the feed is well-formed.
    return ET.fromstring(content)  # noqa: S314


@pytest.fixture
def comic(db: None) -> Comic:
    return Comic.objects.create(
        name="Jesus & Mo",
        slug="jesusandmo",
        language="en",
        url="https://www.jesusandmo.net/",
        rights="Mohammed Jones",
    )


@pytest.fixture
def releases(comic: Comic) -> list[Release]:
    return [
        Release.objects.create(comic=comic, pub_date=dt.date.today()),
        Release.objects.create(comic=comic, pub_date=dt.date.today()),
    ]


@pytest.fixture
def subscription(user: User, comic: Comic) -> Subscription:
    profile: UserProfile = user.comics_profile  # pyright: ignore[reportAttributeAccessIssue, reportUnknownMemberType]
    return Subscription.objects.create(userprofile=profile, comic=comic)


def test_my_comics_feed_requires_secret_key(db: None, client: Client) -> None:
    response = client.get("/my/feed/")

    assert response.status_code == 404


def test_my_comics_feed_with_wrong_secret_key(
    db: None, client: Client, user: User
) -> None:
    response = client.get("/my/feed/", {"key": "wrong"})

    assert response.status_code == 404


def test_my_comics_feed_is_valid_atom(
    client: Client,
    user: User,
    releases: list[Release],
    subscription: Subscription,
) -> None:
    response = client.get("/my/feed/", {"key": "s3cretk3y"})

    assert response.status_code == 200
    assert response["Content-Type"] == "application/atom+xml; charset=utf-8"

    # The feed parses even though it contains a comic named "Jesus & Mo".
    feed = parse_feed(response.content)

    assert feed.findtext(f"{ATOM}title") == "My comics"

    links = {link.get("rel"): link.get("href") for link in feed.findall(f"{ATOM}link")}
    assert links["alternate"] == "https://comics.example.com/my/"
    assert links["self"] == "https://comics.example.com/my/feed/?key=s3cretk3y"


def test_my_comics_feed_entries(
    client: Client,
    user: User,
    releases: list[Release],
    subscription: Subscription,
) -> None:
    response = client.get("/my/feed/", {"key": "s3cretk3y"})

    feed = parse_feed(response.content)
    entries = feed.findall(f"{ATOM}entry")
    assert len(entries) == 2

    entry = entries[0]
    title = entry.findtext(f"{ATOM}title")
    assert title is not None
    assert title.startswith("Jesus & Mo published ")

    today = dt.date.today()
    entry_ids = {entry.findtext(f"{ATOM}id") for entry in entries}
    assert entry_ids == {
        f"tag:comics.example.com,{today.isoformat()}:releases/{release.pk}"
        for release in releases
    }

    link = entry.find(f"{ATOM}link")
    assert link is not None
    assert link.get("href") == (
        f"https://comics.example.com/jesusandmo/{today.year}/{today.month}/{today.day}/"
    )

    summary = entry.findtext(f"{ATOM}summary")
    assert summary is not None
    assert "No matching images found." in summary

    assert entry.findtext(f"{ATOM}rights") == "Mohammed Jones"


def test_my_comics_feed_without_subscriptions_has_no_entries(
    client: Client, user: User, releases: list[Release]
) -> None:
    response = client.get("/my/feed/", {"key": "s3cretk3y"})

    feed = parse_feed(response.content)
    assert len(feed.findall(f"{ATOM}entry")) == 0


def test_one_comic_feed_requires_secret_key(
    db: None, client: Client, comic: Comic
) -> None:
    response = client.get("/jesusandmo/feed/")

    assert response.status_code == 404


def test_one_comic_feed_with_unknown_comic(
    db: None, client: Client, user: User
) -> None:
    response = client.get("/unknown/feed/", {"key": "s3cretk3y"})

    assert response.status_code == 404


def test_one_comic_feed_is_valid_atom(
    client: Client, user: User, releases: list[Release]
) -> None:
    response = client.get("/jesusandmo/feed/", {"key": "s3cretk3y"})

    assert response.status_code == 200
    assert response["Content-Type"] == "application/atom+xml; charset=utf-8"

    feed = parse_feed(response.content)

    assert feed.findtext(f"{ATOM}title") == "Comics from Jesus & Mo"

    links = {link.get("rel"): link.get("href") for link in feed.findall(f"{ATOM}link")}
    assert links["alternate"] == "https://comics.example.com/jesusandmo/"
    assert links["self"] == "https://comics.example.com/jesusandmo/feed/?key=s3cretk3y"

    assert len(feed.findall(f"{ATOM}entry")) == 2


def test_one_comic_feed_excludes_other_comics(
    client: Client, user: User, releases: list[Release]
) -> None:
    other_comic = Comic.objects.create(name="Other", slug="other", language="en")
    Release.objects.create(comic=other_comic, pub_date=dt.date.today())

    response = client.get("/jesusandmo/feed/", {"key": "s3cretk3y"})

    feed = parse_feed(response.content)
    titles = [entry.findtext(f"{ATOM}title") for entry in feed.findall(f"{ATOM}entry")]
    assert len(titles) == 2
    assert all(title and title.startswith("Jesus & Mo") for title in titles)


def test_feeds_exclude_old_releases(
    client: Client, user: User, comic: Comic, subscription: Subscription
) -> None:
    old_release = Release.objects.create(comic=comic, pub_date=dt.date(2012, 1, 1))
    Release.objects.filter(pk=old_release.pk).update(
        fetched=dt.datetime(2012, 1, 1, tzinfo=dt.UTC)
    )

    response = client.get("/my/feed/", {"key": "s3cretk3y"})

    feed = parse_feed(response.content)
    assert len(feed.findall(f"{ATOM}entry")) == 0
