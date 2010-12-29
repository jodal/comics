# encoding: utf-8

from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.meta.base import MetaBase

class Meta(MetaBase):
    name = 'Uten Sokker'
    language = 'no'
    url = 'http://nettserier.no/utensokker/'
    start_date = '2009-07-14'
    rights = 'Bjørnar Grandalen'

class Crawler(CrawlerBase):
    history_capable_days = 180
    schedule = 'Sa,Su'
    time_zone = 1

    def crawl(self, pub_date):
        feed = self.parse_feed('http://nettserier.no/utensokker/rss/')
        for entry in feed.for_date(pub_date):
            url = entry.html(entry.description).src('img')
            return CrawlerImage(url)
