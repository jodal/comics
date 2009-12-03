import logging

from comics.comics import get_comic_module_names, get_comic_module
from comics.meta.exceptions import MetaError

logger = logging.getLogger('comics.meta.command')

class MetaLoader(object):
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
            meta = self._get_meta(comic_slug)
            self._load_meta(meta)
        except MetaError, error:
            logger.error(error)
        except Exception, error:
            logger.exception(error)

    def _get_meta(self, comic_slug):
        logger.debug('Importing comic module for %s', comic_slug)
        comic_module = get_comic_module(comic_slug)
        if not hasattr(comic_module, 'Meta'):
            raise MetaError('%s does not have a Meta class' %
                comic_module.__name__)
        return comic_module.Meta()

    def _load_meta(self, meta):
        logger.debug('Syncing comic meta data with database')
        meta.create_comic()
