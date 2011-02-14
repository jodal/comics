from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.meta.base import MetaBase

class Meta(MetaBase):
    name = 'Life With Rippy'
    language = 'en'
    url = 'http://www.rhymes-with-witch.com/'
    start_date = '2006-08-09'
    end_date = '2009-11-25'
    rights = 'r*k*milholland'

class Crawler(CrawlerBase):
    history_capable_date = '2006-08-09'
    schedule = None

    def crawl(self, pub_date):
        pass # Comic no longer published
