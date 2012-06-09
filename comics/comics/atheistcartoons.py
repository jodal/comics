from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.meta.base import MetaBase

class Meta(MetaBase):
    name = 'Atheist Cartoons'
    language = 'en'
    url = 'http://www.atheistcartoons.com/'
    start_date = '2009-01-03'
    end_date = '2011-08-25'
    active = False
    rights = 'Atheist Cartoons'

class Crawler(CrawlerBase):
    def crawl(self, pub_date):
        pass # Comic no longer published
