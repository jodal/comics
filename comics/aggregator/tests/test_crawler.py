import datetime

from django.test import TestCase

import pytz

from comics.aggregator import crawler


class CurrentDateWhenLocalTZIsUTCTest(TestCase):
    time_zone_local = 'UTC'
    time_zone_ahead = 'Australia/Sydney'
    time_zone_behind = 'America/New_York'

    def setUp(self):
        self.tz = pytz.timezone(self.time_zone_local)
        self.crawler = crawler.CrawlerBase(None)
        crawler.now = lambda: self.now
        crawler.today = lambda: self.now.today()

    def test_current_date_when_crawler_is_in_local_today(self):
        self.now = self.tz.localize(datetime.datetime(2001, 2, 5, 23, 1, 0))
        self.crawler.time_zone = self.time_zone_local

        today = datetime.date(2001, 2, 5)
        self.assertEqual(self.crawler.current_date, today)

    def test_current_date_when_crawler_is_in_local_tomorrow(self):
        self.now = self.tz.localize(datetime.datetime(2001, 2, 5, 23, 1, 0))
        self.crawler.time_zone = self.time_zone_ahead

        tomorrow = datetime.date(2001, 2, 6)
        self.assertEqual(self.crawler.current_date, tomorrow)

    def test_current_date_when_crawler_is_in_local_yesterday(self):
        self.now = self.tz.localize(datetime.datetime(2001, 2, 5, 0, 59, 0))
        self.crawler.time_zone = self.time_zone_behind

        yesterday = datetime.date(2001, 2, 4)
        self.assertEqual(self.crawler.current_date, yesterday)


class CurrentDateWhenLocalTZIsCETTest(CurrentDateWhenLocalTZIsUTCTest):
    time_zone_local = 'Europe/Oslo'
    time_zone_ahead = 'Australia/Sydney'
    time_zone_behind = 'America/New_York'


class CurrentDateWhenLocalTZIsESTTest(CurrentDateWhenLocalTZIsUTCTest):
    time_zone_local = 'America/New_York'
    time_zone_ahead = 'Europe/Moscow'
    time_zone_behind = 'America/Los_Angeles'
