from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.meta.base import MetaBase

class Meta(MetaBase):
    name = 'Pet Peevy'
    language = 'en'
    url = 'http://dobbcomics.com/'
    rights = 'Rob Snyder'

class Crawler(CrawlerBase):
    schedule = None

    def crawl(self, pub_date):
        pass # Comic no longer pubslshed
