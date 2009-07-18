import datetime as dt
import logging

from comics.common.models import Comic
from comics.crawler.utils import get_comic_module

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
            logger.error('Loading all comics is not implemented yet, '
                'use "-c COMIC".')
            return [] # TODO Add all comic slugs
        else:
            return comic_slugs

    def _try_load_comic_meta(self, comic_slug):
        try:
            self._load_comic_meta(comic_slug)
        except Exception, error:
            logger.exception(error)

    def _load_comic_meta(self, comic_slug):
        logger.debug('Importing comic module')
        comic_module = get_comic_module(comic_slug)
        comic_meta = comic_module.ComicMeta()
        logger.debug('Loading comic into database')
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
    schedule = None
    time_zone = None
    rights = None

    @property
    def slug(self):
        return self.__module__.split('.')[-1]

    def create_comic(self):
        comic = Comic(
            name=self.name,
            slug=self.slug,
            language=self.language,
            url=self.url)
        if self.start_date:
            comic.start_date = self._get_date(self.start_date)
        if self.end_date:
            comic.end_date = self._get_date(self.end_date)
        if self.history_capable_date:
            comic.history_capable_date = self._get_date(
                self.history_capable_date)
        if self.history_capable_days:
            comic.history_capable_days = self.history_capable_days
        if self.has_reruns:
            comic.has_reruns = self.has_reruns
        if self.schedule:
            comic.schedule = self.schedule
        if self.time_zone:
            comic.time_zone = self.time_zone
        if self.rights:
            comic.rights = self.rights
        comic.save()

    def _get_date(self, date):
        return dt.datetime.strptime(date, '%Y-%m-%d').date()
