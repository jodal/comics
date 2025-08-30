import pytest
import datetime
from unittest import mock

from django.test import TestCase

from comics.aggregator import command
from comics.aggregator.crawler import CrawlerRelease
from comics.aggregator.exceptions import ComicsError
from comics.core.models import Comic


def create_comics():
    Comic.objects.create(slug="xkcd")
    Comic.objects.create(slug="sinfest")


class AggregatorConfigTestCase(TestCase):
    def setUp(self):
        create_comics()
        self.cc = command.AggregatorConfig()

    def test_init(self):
        assert len(self.cc.comics) == 0
        assert self.cc.from_date is None
        assert self.cc.to_date is None

    def test_init_invalid(self):
        pytest.raises(AttributeError, command.AggregatorConfig)

    def test_set_from_date(self):
        from_date = datetime.date(2008, 3, 11)
        self.cc._set_from_date(from_date)
        assert from_date == self.cc.from_date

    def test_set_from_date_from_string(self):
        from_date = datetime.date(2008, 3, 11)
        self.cc._set_from_date(str(from_date))
        assert from_date == self.cc.from_date

    def test_set_to_date(self):
        to_date = datetime.date(2008, 3, 11)
        self.cc._set_to_date(to_date)
        assert to_date == self.cc.to_date

    def test_set_to_date_from_string(self):
        to_date = datetime.date(2008, 3, 11)
        self.cc._set_to_date(str(to_date))
        assert to_date == self.cc.to_date

    def test_validate_dates_valid(self):
        self.cc.from_date = datetime.date(2008, 3, 11)
        self.cc.to_date = datetime.date(2008, 3, 11)
        assert self.cc._validate_dates()

        self.cc.from_date = datetime.date(2008, 2, 29)
        self.cc.to_date = datetime.date(2008, 3, 2)
        assert self.cc._validate_dates()

    def test_validate_dates_invalid(self):
        self.cc.from_date = datetime.date(2008, 3, 11)
        self.cc.to_date = datetime.date(2008, 3, 10)
        pytest.raises(ComicsError, self.cc._validate_dates)

    def test_get_comic_by_slug_valid(self):
        expected = Comic.objects.get(slug="xkcd")
        result = self.cc._get_comic_by_slug("xkcd")
        assert expected == result

    def test_get_comic_by_slug_invalid(self):
        self.assertRaises(ComicsError, self.cc._get_comic_by_slug, "not slug")

    def test_set_comics_to_crawl_two(self):
        comic1 = Comic.objects.get(slug="xkcd")
        comic2 = Comic.objects.get(slug="sinfest")
        self.cc.set_comics_to_crawl(["xkcd", "sinfest"])
        assert len(self.cc.comics) == 2
        assert comic1 in self.cc.comics
        assert comic2 in self.cc.comics

    def test_set_comics_to_crawl_all(self):
        all_count = Comic.objects.count()

        self.cc.set_comics_to_crawl(None)
        assert all_count == len(self.cc.comics)

        self.cc.set_comics_to_crawl([])
        assert all_count == len(self.cc.comics)


class ComicAggregatorTestCase(TestCase):
    def setUp(self):
        create_comics()
        config = command.AggregatorConfig()
        config.set_comics_to_crawl(None)
        self.aggregator = command.Aggregator(config)
        self.aggregator.identifier = "slug"

        self.comic = mock.Mock()
        self.comic.slug = "slug"
        self.crawler_mock = mock.Mock()
        self.crawler_mock.comic = self.comic
        self.downloader_mock = mock.Mock()

    def test_init(self):
        assert isinstance(self.aggregator.config, command.AggregatorConfig)

    def test_init_options(self):
        options_mock = mock.Mock()
        options_mock.comic_slugs = None
        options_mock.from_date = None
        options_mock.to_date = None
        options_mock.get.return_value = None

        result = command.Aggregator(options=options_mock)

        assert len(self.aggregator.config.comics) == len(result.config.comics)
        assert self.aggregator.config.from_date == result.config.from_date
        assert self.aggregator.config.to_date == result.config.to_date

    def test_init_invalid_config(self):
        pytest.raises(AssertionError, command.Aggregator)

    def test_crawl_one_comic_one_date(self):
        pub_date = datetime.date(2008, 3, 1)
        crawler_release = CrawlerRelease(self.comic, pub_date)
        self.crawler_mock.get_crawler_release.return_value = crawler_release

        self.aggregator._crawl_one_comic_one_date(self.crawler_mock, pub_date)

        assert self.crawler_mock.get_crawler_release.call_count == 1
        self.crawler_mock.get_crawler_release.assert_called_with(pub_date)

    def test_download_release(self):
        crawler_release = CrawlerRelease(self.comic, datetime.date(2008, 3, 1))
        self.aggregator._get_downloader = lambda: self.downloader_mock

        self.aggregator._download_release(crawler_release)

        assert self.downloader_mock.download.call_count == 1
        self.downloader_mock.download.assert_called_with(crawler_release)

    def test_get_valid_date_from_history_capable(self):
        expected = datetime.date(2008, 3, 1)
        self.crawler_mock.comic = Comic.objects.get(slug="xkcd")
        self.crawler_mock.history_capable = expected
        self.crawler_mock.current_date = datetime.date(2008, 4, 1)

        result = self.aggregator._get_valid_date(
            self.crawler_mock, datetime.date(2008, 2, 1)
        )

        assert expected == result

    def test_get_valid_date_from_config(self):
        expected = datetime.date(2008, 3, 1)
        self.crawler_mock.comic = Comic.objects.get(slug="xkcd")
        self.crawler_mock.history_capable = datetime.date(2008, 1, 1)
        self.crawler_mock.current_date = datetime.date(2008, 4, 1)

        result = self.aggregator._get_valid_date(self.crawler_mock, expected)

        assert expected == result

    def test_get_crawler(self):
        pass  # TODO

    def test_get_downloader(self):
        pass  # TODO

    def test_aggregate_one_comic(self):
        pass  # TODO

    def test_start(self):
        pass  # TODO
