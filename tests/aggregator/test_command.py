import datetime as dt
from unittest import mock

import pytest
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

    def test_init(self):
        config = command.AggregatorConfig()
        assert config.comic_slugs == []
        assert config.from_date is None
        assert config.to_date is None

    def test_set_from_date(self):
        config = command.AggregatorConfig.from_options(from_date=dt.date(2008, 3, 11))
        assert config.from_date == dt.date(2008, 3, 11)

    def test_set_from_date_from_string(self):
        config = command.AggregatorConfig.from_options(from_date="2008-03-11")
        assert config.from_date == dt.date(2008, 3, 11)

    def test_set_to_date(self):
        config = command.AggregatorConfig.from_options(to_date=dt.date(2008, 3, 11))
        assert config.to_date == dt.date(2008, 3, 11)

    def test_set_to_date_from_string(self):
        config = command.AggregatorConfig.from_options(to_date="2008-03-11")
        assert config.to_date == dt.date(2008, 3, 11)

    def test_validate_dates_valid(self):
        command.AggregatorConfig.from_options(
            from_date=dt.date(2008, 3, 11),
            to_date=dt.date(2008, 3, 11),
        )
        command.AggregatorConfig.from_options(
            from_date=dt.date(2008, 2, 29),
            to_date=dt.date(2008, 3, 2),
        )

    def test_validate_dates_invalid(self):
        with pytest.raises(ComicsError):
            command.AggregatorConfig.from_options(
                from_date=dt.date(2008, 3, 11),
                to_date=dt.date(2008, 3, 10),
            )

    def test_comic_by_slug_valid(self):
        config = command.AggregatorConfig.from_options(comic_slugs=["xkcd"])
        assert config.comics == [Comic.objects.get(slug="xkcd")]

    def test_comic_by_slug_invalid(self):
        config = command.AggregatorConfig.from_options(comic_slugs=["not slug"])

        with pytest.raises(ComicsError):
            config.comics  # noqa: B018

    def test_all_comics(self):
        comic1 = Comic.objects.get(slug="xkcd")
        comic2 = Comic.objects.get(slug="sinfest")

        config = command.AggregatorConfig.from_options()

        assert len(config.comic_slugs) == 0
        assert len(config.comics) == 2
        assert comic1 in config.comics
        assert comic2 in config.comics


class ComicAggregatorTestCase(TestCase):
    def setUp(self):
        create_comics()
        config = command.AggregatorConfig()
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
        result = command.Aggregator(
            options={
                "comics_slugs": None,
                "from_date": None,
                "to_date": None,
            }
        )

        assert len(self.aggregator.config.comics) == len(result.config.comics)
        assert self.aggregator.config.from_date == result.config.from_date
        assert self.aggregator.config.to_date == result.config.to_date

    def test_init_invalid_config(self):
        pytest.raises(AssertionError, command.Aggregator)

    def test_crawl_one_comic_one_date(self):
        pub_date = dt.date(2008, 3, 1)
        crawler_release = CrawlerRelease(self.comic, pub_date)
        self.crawler_mock.get_crawler_release.return_value = crawler_release

        self.aggregator._crawl_one_comic_one_date(self.crawler_mock, pub_date)

        assert self.crawler_mock.get_crawler_release.call_count == 1
        self.crawler_mock.get_crawler_release.assert_called_with(pub_date)

    def test_download_release(self):
        crawler_release = CrawlerRelease(self.comic, dt.date(2008, 3, 1))
        self.aggregator._get_downloader = lambda: self.downloader_mock

        self.aggregator._download_release(crawler_release)

        assert self.downloader_mock.download.call_count == 1
        self.downloader_mock.download.assert_called_with(crawler_release)

    def test_get_valid_date_from_history_capable(self):
        expected = dt.date(2008, 3, 1)
        self.crawler_mock.comic = Comic.objects.get(slug="xkcd")
        self.crawler_mock.history_capable = expected
        self.crawler_mock.current_date = dt.date(2008, 4, 1)

        result = self.aggregator._get_valid_date(self.crawler_mock, dt.date(2008, 2, 1))

        assert expected == result

    def test_get_valid_date_from_config(self):
        expected = dt.date(2008, 3, 1)
        self.crawler_mock.comic = Comic.objects.get(slug="xkcd")
        self.crawler_mock.history_capable = dt.date(2008, 1, 1)
        self.crawler_mock.current_date = dt.date(2008, 4, 1)

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
