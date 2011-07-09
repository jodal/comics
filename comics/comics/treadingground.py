from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.meta.base import MetaBase

class Meta(MetaBase):
    name = 'Treading Ground'
    language = 'en'
    url = 'http://www.treadingground.com/'
    start_date = '2003-10-12'
    rights = 'Nick Wright'

class Crawler(CrawlerBase):
    history_capable_days = 30
    schedule = 'Mo,We,Fr'
    time_zone = -5

    def crawl(self, pub_date):
        pass
