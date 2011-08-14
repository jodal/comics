from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.meta.base import MetaBase

class Meta(MetaBase):
    name = 'Idiot Comics'
    language = 'en'
    url = 'http://www.idiotcomics.com/'
    active = False
    start_date = '2006-09-08'
    end_date = '2010-02-15'
    rights = 'Robert Sergel'

class Crawler(CrawlerBase):
    def crawl(self, pub_date):
        pass # Comic no longer published
