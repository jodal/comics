import logging

from comics.comics import get_comic_module_names, get_comic_module
from comics.core.exceptions import ComicDataError

logger = logging.getLogger('comics.core.comic_data')

class ComicDataLoader(object):
    def __init__(self, options):
        self.include_inactive = self._get_include_inactive(options)
        self.comic_slugs = self._get_comic_slugs(options)

    def start(self):
        for comic_slug in self.comic_slugs:
            logger.info('Loading comic data for %s', comic_slug)
            self._try_load_comic_data(comic_slug)

    def stop(self):
        pass

    def _get_include_inactive(self, options):
        comic_slugs = options.get('comic_slugs', None)
        if comic_slugs is None or len(comic_slugs) == 0:
            logger.debug('Excluding inactive comics')
            return False
        else:
            logger.debug('Including inactive comics')
            return True

    def _get_comic_slugs(self, options):
        comic_slugs = options.get('comic_slugs', None)
        if comic_slugs is None or len(comic_slugs) == 0:
            logger.debug('Load targets: all comics')
            return get_comic_module_names()
        else:
            logger.debug('Load targets: %s', comic_slugs)
            return comic_slugs

    def _try_load_comic_data(self, comic_slug):
        try:
            data = self._get_data(comic_slug)
            if self._should_load_data(data):
                self._load_data(data)
            else:
                logger.debug('Skipping inactive comic')
        except ComicDataError, error:
            logger.error(error)
        except Exception, error:
            logger.exception(error)

    def _get_data(self, comic_slug):
        logger.debug('Importing comic module for %s', comic_slug)
        comic_module = get_comic_module(comic_slug)
        if not hasattr(comic_module, 'Meta'):
            raise ComicDataError('%s does not have a Meta class' %
                comic_module.__name__)
        return comic_module.Meta()

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
        logger.debug('Syncing comic data with database')
        data.create_comic()
