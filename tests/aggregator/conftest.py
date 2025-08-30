import pytest

from comics.core.models import Comic


@pytest.fixture
def comics(db: None) -> list[Comic]:
    return [
        Comic.objects.create(slug="xkcd"),
        Comic.objects.create(slug="sinfest"),
    ]
