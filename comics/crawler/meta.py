import logging

from django.conf import settings

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
