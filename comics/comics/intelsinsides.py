from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.meta.base import MetaBase

class Meta(MetaBase):
    name = "Intel's Insides"
    language = 'en'
    url = 'http://www.intelsinsides.com/'
    active = False
    start_date = '2009-09-21'
    end_date = '2010-04-15'
    rights = 'Steve Lait'

class Crawler(CrawlerBase):
    def crawl(self, pub_date):
        pass # Comic no longer published
