from comics.aggregator.crawler import CrawlerBase
from comics.meta.base import MetaBase

class Meta(MetaBase):
    name = 'The Perry Bible Fellowship'
    language = 'en'
    url = 'http://www.pbfcomics.com/'
    active = False
    start_date = '2001-01-01'
    rights = 'Nicholas Gurewitch'

class Crawler(CrawlerBase):
    def crawl(self, pub_date):
        pass # Comic no longer published
