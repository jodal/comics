from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.meta.base import MetaBase

class Meta(MetaBase):
    name = 'Treading Ground'
    language = 'en'
    url = 'http://www.treadingground.com/'
    active = False
    start_date = '2003-10-12'
    rights = 'Nick Wright'

class Crawler(CrawlerBase):
    def crawl(self, pub_date):
        pass # Comic no longer published
