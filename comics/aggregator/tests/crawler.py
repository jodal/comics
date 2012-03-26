import datetime
from django.utils import unittest

from comics.aggregator import crawler

class CurrentDateWhenLocalTZIsUTCTest(unittest.TestCase):
    time_zone = 0 # UTC+0, GMT

    def setUp(self):
        self.now = datetime.datetime(2001, 2, 5, 22, 1, 0)
        crawler.now = lambda: self.now
        crawler.today = lambda: self.now.date()
        crawler.utc_offset_in_s = -3600 * self.time_zone

    def test_current_date_when_crawler_is_in_local_today(self):
        c = crawler.CrawlerBase(None)
        c.time_zone = self.time_zone

        today = self.now.date()
        self.assertEqual(c.current_date, today)

    def test_current_date_when_crawler_is_in_local_tomorrow(self):
        c = crawler.CrawlerBase(None)
        c.time_zone = self.time_zone + 5

        tomorrow = self.now.date() + datetime.timedelta(days=1)
        self.assertEqual(c.current_date, tomorrow)

    def test_current_date_when_crawler_is_in_local_yesterday(self):
        self.now = datetime.datetime(2001, 2, 5, 2, 1, 0)

        c = crawler.CrawlerBase(None)
        c.time_zone = self.time_zone - 5

        yesterday = self.now.date() - datetime.timedelta(days=1)
        self.assertEqual(c.current_date, yesterday)

class CurrentDateWhenLocalTZIsCETTest(CurrentDateWhenLocalTZIsUTCTest):
    time_zone = 1 # UTC+1, CET

class CurrentDateWhenLocalTZIsESTTest(CurrentDateWhenLocalTZIsUTCTest):
    time_zone = -5 # UTC-5, EST
