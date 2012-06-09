from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.meta.base import MetaBase

class Meta(MetaBase):
    name = 'Bunny'
    language = 'en'
    url = 'http://bunny-comic.com/'
    start_date = '2004-08-22'
    end_date = '2011-11-20'
    active = False
    rights = 'H. Davies, CC BY-NC-SA'

class Crawler(CrawlerBase):
    def crawl(self, pub_date):
        pass # Comic no longer published
