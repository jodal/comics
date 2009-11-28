"""Aggregator which fetches comic strips from the web"""

import datetime as dt
import logging
import socket

from django.conf import settings

from comics.aggregator.exceptions import StripAlreadyExists
from comics.core.exceptions import ComicsError
from comics.comics import get_comic_module

logger = logging.getLogger('comics.aggregator.command')
socket.setdefaulttimeout(10)

class ComicCrawlerRunner(object):
    def __init__(self, config=None, optparse_options=None):
        if config is None and optparse_options is not None:
            self.config = ComicCrawlerRunnerConfig(optparse_options)
        else:
            assert isinstance(config, ComicCrawlerRunnerConfig)
            self.config = config

    def start(self):
        for comic in self.config.comics:
            self._try_crawl_one_comic(comic)

    def stop(self):
        pass

    def _try_crawl_one_comic(self, comic):
        try:
            self._crawl_one_comic(comic)
        except Exception, error:
            logger.exception(error)

    def _crawl_one_comic(self, comic):
        comic_crawler = self._get_comic_crawler(comic)
        pub_date = self._get_from_date(comic)
        logger.info('Crawling %s from %s to %s'
            % (comic.slug, pub_date, self.config.to_date))
        while pub_date <= self.config.to_date:
            self._try_crawl_one_comic_one_date(comic_crawler, pub_date)
            pub_date += dt.timedelta(days=1)
        self._update_strip_titles(comic_crawler)

    def _get_comic_crawler(self, comic):
        module = get_comic_module(comic.slug)
        return module.ComicCrawler(comic)

    def _get_from_date(self, comic):
        if self.config.from_date < comic.history_capable():
            logger.info('Adjusting from date to %s because of limited ' +
                'history capability', comic.history_capable())
            return comic.history_capable()
        else:
            return self.config.from_date

    def _try_crawl_one_comic_one_date(self, comic_crawler, pub_date):
        try:
            logger.debug('Crawling %s for %s',
                comic_crawler.comic.slug, pub_date)
            self._crawl_one_comic_one_date(comic_crawler, pub_date)
        except ComicsError, error:
            logger.info(error)
        except IOError, error:
            logger.warning(error)
        except Exception, error:
            logger.exception(error)

    def _crawl_one_comic_one_date(self, comic_crawler, pub_date):
        comic_crawler.get_url(pub_date)
        logger.debug('Strip URL: %s', comic_crawler.url)
        logger.debug('Strip title: %s', comic_crawler.title)
        logger.debug('Strip text: %s', comic_crawler.text)
        comic_crawler.get_strip()
        logger.info('Strip saved (%s/%s)', comic_crawler.comic.slug, pub_date)

    def _update_strip_titles(self, comic_crawler):
        if hasattr(comic_crawler, 'update_titles'):
            num_updated = comic_crawler.update_titles()
            logger.info('%d title(s) updated', num_updated)
            return num_updated

class ComicCrawlerRunnerConfig(object):
    DATE_FORMAT = '%Y-%m-%d'

    def __init__(self, options=None):
        self.comics = []
        self.from_date = today()
        self.to_date = today()
        if options is not None:
            self.setup(options)

    def setup(self, options):
        self.set_comics_to_crawl(options.get('comic_slugs', None))
        self.set_date_interval(
            options.get('from_date', None),
            options.get('to_date', None))

    def set_comics_to_crawl(self, comic_slugs):
        from comics.core.models import Comic
        if comic_slugs is None or len(comic_slugs) == 0:
            logger.debug('Crawl targets: all comics')
            self.comics = Comic.objects.all()
        else:
            comics = []
            for comic_slug in comic_slugs:
                comics.append(self._get_comic_by_slug(comic_slug))
            logger.debug('Crawl targets: %s' % comics)
            self.comics = comics

    def _get_comic_by_slug(self, comic_slug):
        from comics.core.models import Comic
        try:
            comic = Comic.objects.get(slug=comic_slug)
        except Comic.DoesNotExist:
            error_msg = 'Comic %s not found' % comic_slug
            logger.error(error_msg)
            raise ComicsError(error_msg)
        return comic

    def set_date_interval(self, from_date, to_date):
        self._set_from_date(from_date)
        self._set_to_date(to_date)
        self._validate_dates()

    def _set_from_date(self, from_date):
        if from_date is not None:
            self.from_date = dt.datetime.strptime(
                str(from_date), self.DATE_FORMAT).date()
        logger.debug('From date: %s', self.from_date)

    def _set_to_date(self, to_date):
        if to_date is not None:
            self.to_date = dt.datetime.strptime(
                str(to_date), self.DATE_FORMAT).date()
        logger.debug('To date: %s', self.to_date)

    def _validate_dates(self):
        if self.from_date > self.to_date:
            error_msg = 'From date (%s) after to date (%s)' % (
                self.from_date, self.to_date)
            logger.error(error_msg)
            raise ComicsError(error_msg)
        else:
            return True

# For testability
today = dt.date.today
