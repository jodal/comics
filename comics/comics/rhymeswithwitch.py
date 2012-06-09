from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.meta.base import MetaBase

class Meta(MetaBase):
    name = 'rhymes with witch'
    language = 'en'
    url = 'http://www.rhymes-with-witch.com/'
    start_date = '2006-08-09'
    end_date = '2011-11-21'
    active = False
    rights = 'r*k*milholland'

class Crawler(CrawlerBase):
    def crawl(self, pub_date):
        pass # Comic no longer published
