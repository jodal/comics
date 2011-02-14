from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.meta.base import MetaBase

class Meta(MetaBase):
    name = 'InkTank'
    language = 'en'
    url = 'http://www.inktank.com/'
    start_date = '2008-03-31'
    end_date = '2010-07-02'
    rights = 'Barry T. Smith'

class Crawler(CrawlerBase):
    schedule = None
    time_zone = -8

    def crawl(self, pub_date):
        pass # Comic no longer published
