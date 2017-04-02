"""Aggregator which fetches comic releases from the web"""

import datetime
import logging
import socket

from comics.aggregator.downloader import ReleaseDownloader
from comics.comics import get_comic_module
from comics.core.exceptions import ComicsError

logger = logging.getLogger('comics.aggregator.command')
socket.setdefaulttimeout(10)


def log_errors(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ComicsError, error:
            logger.info(error)
        except Exception, error:
            logger.exception(u'%s: %s', args[0].identifier, error)
    return inner


class Aggregator(object):
    def __init__(self, config=None, options=None):
        if config is None and options is not None:
            self.config = AggregatorConfig(options)
        else:
            assert isinstance(config, AggregatorConfig)
            self.config = config

    def start(self):
        start_time = datetime.datetime.now()
        for comic in self.config.comics:
            self.identifier = comic.slug
            self._aggregate_one_comic(comic)
        ellapsed_time = datetime.datetime.now() - start_time
        logger.info('Crawling completed in %s', ellapsed_time)

    def stop(self):
        pass

    @log_errors
    def _aggregate_one_comic(self, comic):
        crawler = self._get_crawler(comic)
        from_date = self._get_valid_date(crawler, self.config.from_date)
        to_date = self._get_valid_date(crawler, self.config.to_date)
        if from_date != to_date:
            logger.info(
                '%s: Crawling from %s to %s', comic.slug, from_date, to_date)
        pub_date = from_date
        while pub_date <= to_date:
            self.identifier = u'%s/%s' % (comic.slug, pub_date)
            crawler_release = self._crawl_one_comic_one_date(crawler, pub_date)
            if crawler_release:
                self._download_release(crawler_release)
            pub_date += datetime.timedelta(days=1)

    @log_errors
    def _crawl_one_comic_one_date(self, crawler, pub_date):
        logger.debug('Crawling %s for %s', crawler.comic.slug, pub_date)
        crawler_release = crawler.get_crawler_release(pub_date)
        if crawler_release:
            logger.debug('Release: %s', crawler_release.identifier)
            for image in crawler_release.images:
                logger.debug('Image URL: %s', image.url)
                logger.debug('Image title: %s', image.title)
                logger.debug('Image text: %s', image.text)
        return crawler_release

    @log_errors
    def _download_release(self, crawler_release):
        logger.debug('Downloading %s', crawler_release.identifier)
        downloader = self._get_downloader()
        downloader.download(crawler_release)
        logger.info('%s: Release saved', crawler_release.identifier)

    def _get_downloader(self):
        return ReleaseDownloader()

    def _get_crawler(self, comic):
        module = get_comic_module(comic.slug)
        return module.Crawler(comic)

    def _get_valid_date(self, crawler, date):
        if date is None:
            return crawler.current_date
        elif date < crawler.history_capable:
            logger.info(
                '%s: Adjusting date from %s to %s because of ' +
                'limited history capability',
                crawler.comic.slug, date, crawler.history_capable)
            return crawler.history_capable
        elif date > crawler.current_date:
            logger.info(
                '%s: Adjusting date from %s to %s because the given ' +
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
            self.from_date = datetime.datetime.strptime(
                str(from_date), self.DATE_FORMAT).date()
        logger.debug('From date: %s', self.from_date)

    def _set_to_date(self, to_date):
        if to_date is not None:
            self.to_date = datetime.datetime.strptime(
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
