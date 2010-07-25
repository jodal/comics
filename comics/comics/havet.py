from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.meta.base import MetaBase

import re

class Meta(MetaBase):
    name = 'Havet'
    language = 'no'
    url = 'http://nettserier.no/havet'
    start_date = '2007-09-27'
    rights = 'Unknown'

class Crawler(CrawlerBase):
    history_capable_days = 180
    schedule = 'Th'
    time_zone = 2

    def crawl(self, pub_date):
        feed = self.parse_feed('http://nettserier.no/havet/rss/')
        for entry in feed.for_date(pub_date):
            url = entry.html(entry.description).src('img')
            return CrawlerImage(url)
