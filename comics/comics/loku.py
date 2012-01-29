from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.meta.base import MetaBase

class Meta(MetaBase):
    name = 'LO-KU'
    language = 'en'
    url = 'http://www.lo-ku.com/'
    start_date = '2009-06-15'
    active = False
    rights = 'Thomas & Daniel Drinnen'

class Crawler(CrawlerBase):
    def crawl(self, pub_date):
        pass # Comic no longer published
