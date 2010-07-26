from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.meta.base import MetaBase

class Meta(MetaBase):
    name = '8-Bit Theater'
    language = 'en'
    url = 'http://www.nuklearpower.com/'
    start_date = '2001-03-02'
    end_date = '2010-06-01'
    rights = 'Brian Clevinger'

class Crawler(CrawlerBase):
    def crawl(self, pub_date):
        pass # Comic no longer published
