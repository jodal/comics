import datetime as dt
import pmock

from django.test import TestCase

from comics.aggregator import command
from comics.aggregator.crawler import CrawlerRelease
from comics.aggregator.exceptions import ComicsError
from comics.core.models import Comic

class AggregatorConfigTestCase(TestCase):
    fixtures = ['test_comics.json']

    def setUp(self):
        self.cc = command.AggregatorConfig()

    def test_init(self):
        self.assertEquals(0, len(self.cc.comics))
        self.assertEquals(None, self.cc.from_date)
        self.assertEquals(None, self.cc.to_date)

    def test_init_invalid(self):
        self.assertRaises(AttributeError,
            command.AggregatorConfig, options=True)

    def test_set_from_date(self):
        from_date = dt.date(2008, 3, 11)
        self.cc._set_from_date(from_date)
        self.assertEquals(from_date, self.cc.from_date)

    def test_set_from_date_from_string(self):
        from_date = dt.date(2008, 3, 11)
        self.cc._set_from_date(str(from_date))
        self.assertEquals(from_date, self.cc.from_date)

    def test_set_to_date(self):
        to_date = dt.date(2008, 3, 11)
        self.cc._set_to_date(to_date)
        self.assertEquals(to_date, self.cc.to_date)

    def test_set_to_date_from_string(self):
        to_date = dt.date(2008, 3, 11)
        self.cc._set_to_date(str(to_date))
        self.assertEquals(to_date, self.cc.to_date)

    def test_validate_dates_valid(self):
        self.cc.from_date = dt.date(2008, 3, 11)
        self.cc.to_date = dt.date(2008, 3, 11)
        self.assertTrue(self.cc._validate_dates())

        self.cc.from_date = dt.date(2008, 2, 29)
        self.cc.to_date = dt.date(2008, 3, 2)
        self.assertTrue(self.cc._validate_dates())

    def test_validate_dates_invalid(self):
        self.cc.from_date = dt.date(2008, 3, 11)
        self.cc.to_date = dt.date(2008, 3, 10)
        self.assertRaises(ComicsError, self.cc._validate_dates)

    def test_get_comic_by_slug_valid(self):
        expected = Comic.objects.get(slug='xkcd')
        result = self.cc._get_comic_by_slug('xkcd')
        self.assertEquals(expected, result)

    def test_get_comic_by_slug_invalid(self):
        self.assertRaises(ComicsError, self.cc._get_comic_by_slug, 'not slug')

    def test_set_comics_to_crawl_two(self):
        comic1 = Comic.objects.get(slug='xkcd')
        comic2 = Comic.objects.get(slug='sinfest')
        self.cc.set_comics_to_crawl(['xkcd', 'sinfest'])
        self.assertEquals(2, len(self.cc.comics))
        self.assert_(comic1 in self.cc.comics)
        self.assert_(comic2 in self.cc.comics)

    def test_set_comics_to_crawl_all(self):
        all_count = Comic.objects.count()

        self.cc.set_comics_to_crawl(None)
        self.assertEquals(all_count, len(self.cc.comics))

        self.cc.set_comics_to_crawl([])
        self.assertEquals(all_count, len(self.cc.comics))

class ComicAggregatorTestCase(TestCase):
    fixtures = ['test_comics.json']

    def setUp(self):
        config = command.AggregatorConfig()
        config.set_comics_to_crawl(None)
        self.aggregator = command.Aggregator(config)
        self.aggregator.identifier = 'slug'

        self.comic = pmock.Mock()
        self.comic.slug = 'slug'
        self.crawler_mock = pmock.Mock()
        self.crawler_mock.comic = self.comic
        self.downloader_mock = pmock.Mock()

    def test_init(self):
        self.assert_(isinstance(self.aggregator.config,
            command.AggregatorConfig))

    def test_init_optparse_config(self):
        optparse_options_mock = pmock.Mock()
        optparse_options_mock.comic_slugs = None
        optparse_options_mock.from_date = None
        optparse_options_mock.to_date = None
        optparse_options_mock.stubs().method('get').will(
            pmock.return_value(None))

        result = command.Aggregator(optparse_options=optparse_options_mock)

        self.assertEquals(len(self.aggregator.config.comics),
            len(result.config.comics))
        self.assertEquals(self.aggregator.config.from_date,
            result.config.from_date)
        self.assertEquals(self.aggregator.config.to_date,
            result.config.to_date)

    def test_init_invalid_config(self):
        self.assertRaises(AssertionError, command.Aggregator)

    def test_crawl_one_comic_one_date(self):
        pub_date = dt.date(2008, 3, 1)
        crawler_release = CrawlerRelease(self.comic, pub_date)
        self.crawler_mock.expects(
            pmock.once()).get_crawler_release(pmock.eq(pub_date)).will(
            pmock.return_value(crawler_release))

        self.aggregator._crawl_one_comic_one_date(
            self.crawler_mock, pub_date)

        self.crawler_mock.verify()

    def test_download_release(self):
        crawler_release = CrawlerRelease(self.comic, dt.date(2008, 3, 1))
        self.downloader_mock.expects(
            pmock.once()).download(pmock.eq(crawler_release))
        self.aggregator._get_downloader = lambda: self.downloader_mock

        self.aggregator._download_release(crawler_release)

        self.downloader_mock.verify()

    def test_get_valid_date_from_history_capable(self):
        expected = dt.date(2008, 3, 1)
        self.crawler_mock.comic = Comic.objects.get(slug='xkcd')
        self.crawler_mock.history_capable = expected
        self.crawler_mock.current_date = dt.date(2008, 4, 1)

        result = self.aggregator._get_valid_date(
            self.crawler_mock, dt.date(2008, 2, 1))

        self.assertEquals(expected, result)

    def test_get_valid_date_from_config(self):
        expected = dt.date(2008, 3, 1)
        self.crawler_mock.comic = Comic.objects.get(slug='xkcd')
        self.crawler_mock.history_capable = dt.date(2008, 1, 1)
        self.crawler_mock.current_date = dt.date(2008, 4, 1)

        result = self.aggregator._get_valid_date(
            self.crawler_mock, expected)

        self.assertEquals(expected, result)

    def test_get_crawler(self):
        pass # TODO

    def test_get_downloader(self):
        pass # TODO

    def test_aggregate_one_comic(self):
        pass # TODO

    def test_start(self):
        pass # TODO

