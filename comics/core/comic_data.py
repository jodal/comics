import datetime
import logging

from comics.comics import get_comic_module, get_comic_module_names
from comics.core.exceptions import ComicDataError
from comics.core.models import Comic

logger = logging.getLogger("comics.core.comic_data")


class ComicDataBase:
    # Required values
    name = None
    language = None
    url = None

    # Default values
    active = True
    start_date = None
    end_date = None
    rights = ""

    @property
    def slug(self):
        return self.__module__.split(".")[-1]

    def is_previously_loaded(self):
        return bool(Comic.objects.filter(slug=self.slug).count())

    def create_comic(self):
        if self.is_previously_loaded():
            comic = Comic.objects.get(slug=self.slug)
            comic.name = self.name
            comic.language = self.language
            comic.url = self.url
        else:
            comic = Comic(
                name=self.name,
                slug=self.slug,
                language=self.language,
                url=self.url,
            )
        comic.active = self.active
        comic.start_date = self._get_date(self.start_date)
        comic.end_date = self._get_date(self.end_date)
        comic.rights = self.rights
        comic.save()

    def _get_date(self, date):
        if date is None:
            return None
        return datetime.datetime.strptime(date, "%Y-%m-%d").date()


class ComicDataLoader:
    def __init__(self, options):
        self.include_inactive = self._get_include_inactive(options)
        self.comic_slugs = self._get_comic_slugs(options)

    def start(self):
        for comic_slug in self.comic_slugs:
            logger.info("Loading comic data for %s", comic_slug)
            self._try_load_comic_data(comic_slug)

    def stop(self):
        pass

    def _get_include_inactive(self, options):
        comic_slugs = options.get("comic_slugs", None)
        if comic_slugs is None or len(comic_slugs) == 0:
            logger.debug("Excluding inactive comics")
            return False
        else:
            logger.debug("Including inactive comics")
            return True

    def _get_comic_slugs(self, options):
        comic_slugs = options.get("comic_slugs", None)
        if comic_slugs is None or len(comic_slugs) == 0:
            logger.error("No comic given. Use -c option to specify comic(s).")
            return []
        elif "all" in comic_slugs:
            logger.debug("Load targets: all comics")
            return get_comic_module_names()
        else:
            logger.debug("Load targets: %s", comic_slugs)
            return comic_slugs

    def _try_load_comic_data(self, comic_slug):
        try:
            data = self._get_data(comic_slug)
            if self._should_load_data(data):
                self._load_data(data)
            else:
                logger.debug("Skipping inactive comic")
        except ComicDataError as error:
            logger.error(error)
        except Exception as error:
            logger.exception(error)

    def _get_data(self, comic_slug):
        logger.debug("Importing comic module for %s", comic_slug)
        comic_module = get_comic_module(comic_slug)
        if not hasattr(comic_module, "ComicData"):
            raise ComicDataError(
                "%s does not have a ComicData class" % comic_module.__name__
            )
        return comic_module.ComicData()

    def _should_load_data(self, data):
        if data.active:
            return True
        elif self.include_inactive:
            return True
        elif data.is_previously_loaded():
            return True
        else:
            return False

    def _load_data(self, data):
        logger.debug("Syncing comic data with database")
        data.create_comic()
