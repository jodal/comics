import datetime as dt
import logging

from comics.core.models import Comic
from comics.crawler.exceptions import ComicsMetaError
from comics.crawler.utils import get_comic_module_names, get_comic_module

logger = logging.getLogger('comics.crawler.meta')

class ComicMetaLoader(object):
    def __init__(self, options):
        self.comic_slugs = self._get_comic_slugs(options)

    def start(self):
        for comic_slug in self.comic_slugs:
            logger.info('Loading meta data for %s', comic_slug)
            self._try_load_comic_meta(comic_slug)

    def stop(self):
        pass

    def _get_comic_slugs(self, options):
        comic_slugs = options.get('comic_slugs', None)
        if comic_slugs is None or len(comic_slugs) == 0:
            logger.debug('Load targets: all comics')
            return get_comic_module_names()
        else:
            logger.debug('Load targets: %s', comic_slugs)
            return comic_slugs

    def _try_load_comic_meta(self, comic_slug):
        try:
            comic_meta = self._get_comic_meta(comic_slug)
            self._load_comic_meta(comic_meta)
        except ComicsMetaError, error:
            logger.error(error)
        except Exception, error:
            logger.exception(error)

    def _get_comic_meta(self, comic_slug):
        logger.debug('Importing comic module for %s', comic_slug)
        comic_module = get_comic_module(comic_slug)
        if not hasattr(comic_module, 'ComicMeta'):
            raise ComicsMetaError('%s does not have a ComicMeta class' %
                comic_module.__name__)
        return comic_module.ComicMeta()

    def _load_comic_meta(self, comic_meta):
        logger.debug('Syncing comic meta data with database')
        comic_meta.create_comic()

class BaseComicMeta(object):
    # Required values
    name = None
    language = None
    url = None

    # Default values
    start_date = None
    end_date = None
    history_capable_date = None
    history_capable_days = None
    has_reruns = False
    schedule = ''
    time_zone = None
    rights = ''

    @property
    def slug(self):
        return self.__module__.split('.')[-1]

    def create_comic(self):
        if Comic.objects.filter(slug=self.slug).count():
            comic = Comic.objects.get(slug=self.slug)
            comic.name = self.name
            comic.language = self.language
            comic.url = self.url
        else:
            comic = Comic(
                name=self.name,
                slug=self.slug,
                language=self.language,
                url=self.url)
        comic.start_date = self._get_date(self.start_date)
        comic.end_date = self._get_date(self.end_date)
        comic.history_capable_date = self._get_date(self.history_capable_date)
        comic.history_capable_days = self.history_capable_days
        comic.has_reruns = self.has_reruns
        comic.schedule = self.schedule
        comic.time_zone = self.time_zone
        comic.rights = self.rights
        comic.save()

    def _get_date(self, date):
        if date is None:
            return None
        return dt.datetime.strptime(date, '%Y-%m-%d').date()
