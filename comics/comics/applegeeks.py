from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.meta.base import MetaBase

class Meta(MetaBase):
    name = 'AppleGeeks'
    language = 'en'
    url = 'http://www.applegeeks.com/'
    start_date = '2003-01-01'
    end_date = '2010-11-22'
    active = False
    rights = 'Mohammad Haque & Ananth Panagariya'

class Crawler(CrawlerBase):
    def crawl(self, pub_date):
        pass # Comic no longer published
