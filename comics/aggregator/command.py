"""Aggregator which fetches comic strips from the web"""

import datetime as dt
import logging
import socket

from django.conf import settings

from comics.aggregator.downloader import Downloader
from comics.core.exceptions import ComicsError
from comics.comics import get_comic_module

logger = logging.getLogger('comics.aggregator.command')
socket.setdefaulttimeout(10)

class Aggregator(object):
    def __init__(self, config=None, optparse_options=None):
        if config is None and optparse_options is not None:
            self.config = AggregatorConfig(optparse_options)
        else:
            assert isinstance(config, AggregatorConfig)
            self.config = config

    def start(self):
        for comic in self.config.comics:
            self._try(self._aggregate_one_comic, comic)

    def stop(self):
        pass

    def _aggregate_one_comic(self, comic):
        crawler = self._get_crawler(comic)
        from_date = self._get_valid_date(crawler, self.config.from_date)
        to_date = self._get_valid_date(crawler, self.config.to_date)
        logger.info('%s: Crawling from %s to %s'
            % (comic.slug, from_date, to_date))
        pub_date = from_date
        while pub_date <= to_date:
            strip_metadata = self._try(self._crawl_one_comic_one_date,
                crawler, pub_date)
            if strip_metadata:
                self._try(self._download_strip, strip_metadata)
            pub_date += dt.timedelta(days=1)

    def _crawl_one_comic_one_date(self, crawler, pub_date):
        logger.debug('Crawling %s for %s', crawler.comic.slug, pub_date)
        strip_metadata = crawler.get_strip_metadata(pub_date)
        if strip_metadata:
            logger.debug('Strip: %s', strip_metadata.identifier)
            logger.debug('Strip URL: %s', strip_metadata.url)
            logger.debug('Strip title: %s', strip_metadata.title)
            logger.debug('Strip text: %s', strip_metadata.text)
        return strip_metadata

    def _download_strip(self, strip_metadata):
        logger.debug('Downloading %s', strip_metadata.identifier)
        downloader = self._get_downloader()
        downloader.download_strip(strip_metadata)
        logger.info('%s: Strip saved', strip_metadata.identifier)

    def _get_downloader(self):
        return Downloader()

    def _try(self, func, *args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ComicsError, error:
            logger.info(error)
        except Exception, error:
            logger.exception(error)

    def _get_crawler(self, comic):
        module = get_comic_module(comic.slug)
        return module.Crawler(comic)

    def _get_valid_date(self, crawler, date):
        if date is None:
            return crawler.current_date
        elif date < crawler.history_capable:
            logger.info('%s: Adjusting date from %s to %s because of ' +
                'limited history capability',
                crawler.comic.slug, date, crawler.history_capable)
            return crawler.history_capable
        elif date > crawler.current_date:
            logger.info('%s: Adjusting date from %s to %s because the given ' +
                "date is in the future in the comic's time zone",
                crawler.comic.slug, date, crawler.current_date)
            return crawler.current_date
        else:
            return date


class AggregatorConfig(object):
    DATE_FORMAT = '%Y-%m-%d'

    def __init__(self, options=None):
        self.comics = []
        self.from_date = None
        self.to_date = None
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
        if self.from_date and self.to_date and self.from_date > self.to_date:
            error_msg = 'From date (%s) after to date (%s)' % (
                self.from_date, self.to_date)
            logger.error(error_msg)
            raise ComicsError(error_msg)
        else:
            return True
