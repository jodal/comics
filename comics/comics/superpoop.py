from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.meta.base import MetaBase

class Meta(MetaBase):
    name = 'Superpoop'
    language = 'en'
    url = 'http://www.superpoop.com/'
    active = False
    start_date = '2008-01-01'
    end_date = '2010-12-17'
    rights = 'Drew'

class Crawler(CrawlerBase):
    def crawl(self, pub_date):
        pass # Comic no longer published
