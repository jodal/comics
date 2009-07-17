import datetime as dt
import pmock
import unittest

import django.test

from comics.common.models import Comic
from comics.crawler import supercrawler
from comics.crawler.exceptions import ComicsError

supercrawler.today = lambda: dt.date(2008, 2, 29)

class SuperCrawlerConfigTestCase(unittest.TestCase):
    def setUp(self):
        self.cc = supercrawler.SuperCrawlerConfig()

    def test_init(self):
        self.assertEquals(0, len(self.cc.comics))
        self.assertEquals(supercrawler.today(), self.cc.from_date)
        self.assertEquals(supercrawler.today(), self.cc.to_date)

    def test_init_invalid(self):
        self.assertRaises(AttributeError,
            supercrawler.SuperCrawlerConfig, options=True)

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

class SuperCrawlerTestCase(django.test.TestCase):
    def setUp(self):
        config = supercrawler.SuperCrawlerConfig()
        config.set_comics_to_crawl(None)
        self.super_crawler = supercrawler.SuperCrawler(config)

        comic_crawler_mock = pmock.Mock()
        comic_crawler_mock.url = 'an URL'
        comic_crawler_mock.title = None
        comic_crawler_mock.text = None
        comic_crawler_mock.comic = pmock.Mock()
        comic_crawler_mock.comic.slug = 'xkcd'
        self.comic_crawler_mock = comic_crawler_mock

    def test_init(self):
        self.assert_(isinstance(self.super_crawler.config,
            supercrawler.SuperCrawlerConfig))

    def test_init_optparse_config(self):
        optparse_options_mock = pmock.Mock()
        optparse_options_mock.comic_slugs = None
        optparse_options_mock.from_date = None
        optparse_options_mock.to_date = None
        optparse_options_mock.stubs().method('get').will(
            pmock.return_value(None))

        result = supercrawler.SuperCrawler(
            optparse_options=optparse_options_mock)

        self.assertEquals(len(self.super_crawler.config.comics),
            len(result.config.comics))
        self.assertEquals(self.super_crawler.config.from_date,
            result.config.from_date)
        self.assertEquals(self.super_crawler.config.to_date,
            result.config.to_date)

    def test_init_invalid_config(self):
        self.assertRaises(AssertionError, supercrawler.SuperCrawler)

    def test_update_strip_titles_noop(self):
        expected = None
        self.comic_crawler_mock.expects(
            pmock.once()).update_titles().will(pmock.return_value(expected))

        result = self.super_crawler._update_strip_titles(
            self.comic_crawler_mock)

        self.assertEquals(expected, result)

    def test_update_strip_titles_actual(self):
        expected = 3
        self.comic_crawler_mock.expects(
            pmock.once()).update_titles().will(pmock.return_value(expected))

        result = self.super_crawler._update_strip_titles(
            self.comic_crawler_mock)

        self.comic_crawler_mock.verify()
        self.assertEquals(expected, result)

    def test_crawl_one_comic_one_date(self):
        pub_date = dt.date(2008, 3, 1)
        self.comic_crawler_mock.expects(
            pmock.once()).get_url(pmock.eq(pub_date))
        self.comic_crawler_mock.expects(
            pmock.once()).get_strip().after('get_url')

        self.super_crawler._crawl_one_comic_one_date(
            self.comic_crawler_mock, pub_date)

        self.comic_crawler_mock.verify()

    def test_try_crawl_one_comic_one_date(self):
        pub_date = dt.date(2008, 3, 1)

        self.super_crawler._try_crawl_one_comic_one_date(
            self.comic_crawler_mock, pub_date)

        # TODO Mock _crawl_one_comic_one_date to throw exceptions which should
        # be excepted in _try_crawl_one_comic_one_date.

    def test_get_from_date_from_history_capable(self):
        comic = Comic.objects.get(slug='xkcd')
        expected = dt.date(2008, 3, 1)
        comic.history_capable = lambda: expected

        result = self.super_crawler._get_from_date(comic)

        self.assertEquals(expected, result)

    def test_get_from_date_from_from_date(self):
        comic = Comic.objects.get(slug='xkcd')
        comic.history_capable = lambda: dt.date(2008, 1, 1)

        result = self.super_crawler._get_from_date(comic)

        self.assertEquals(dt.date(2008, 2, 29), result)

    def test_import_by_name(self):
        pass # TODO

    def test_get_comic_crawler(self):
        pass # TODO

    def test_crawl_one_comic(self):
        pass # TODO

    def test_try_crawl_on_comic(self):
        pass # TODO

    def test_start(self):
        pass # TODO

    def test_stop(self):
        pass # TODO
