import datetime as dt

from comics.core.metadata import load_metadata
from comics.core.models import Comic

# A real comic module, and one that no test fixture loads into the database.
REAL_SLUG = "nemi"

UNKNOWN_SLUG = "definitelynotacomic"


def test_loads_the_metadata_a_comic_module_declares(db: None) -> None:
    load_metadata([REAL_SLUG])

    comic = Comic.objects.for_slugs(REAL_SLUG).get()
    assert comic.name == "Nemi (db.no)"
    assert comic.language == "no"
    assert comic.start_date == dt.date(1997, 1, 1)
    assert comic.rights == "Lise Myhre"
    assert comic.active is False


def test_keeps_loading_after_a_comic_module_that_cannot_be_imported(db: None) -> None:
    load_metadata([UNKNOWN_SLUG, REAL_SLUG])

    assert not Comic.objects.for_slugs(UNKNOWN_SLUG).exists()
    assert Comic.objects.for_slugs(REAL_SLUG).exists()
