from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.meta.base import MetaBase

class Meta(MetaBase):
    name = 'Pet Peevy'
    language = 'en'
    url = 'http://dobbcomics.com/'
    active = False
    rights = 'Rob Snyder'

class Crawler(CrawlerBase):
    def crawl(self, pub_date):
        pass # Comic no longer published
