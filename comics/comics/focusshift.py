from comics.aggregator.crawler import CrawlerBase
from comics.meta.base import MetaBase

class Meta(MetaBase):
    name = 'Focus Shift'
    language = 'en'
    url = 'http://www.osnews.com/comics/'
    active = False
    start_date = '2008-01-27'
    rights = 'Thom Holwerda'

class Crawler(CrawlerBase):
    def crawl(self, pub_date):
        pass # Comic no longer published
