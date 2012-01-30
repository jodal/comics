from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.meta.base import MetaBase

class Meta(MetaBase):
    name = 'Bizarro (no)'
    language = 'no'
    url = 'http://underholdning.no.msn.com/tegneserier/bizarro/'
    start_date = '1985-01-01'
    active = False
    rights = 'Dan Piraro'

class Crawler(CrawlerBase):
    def crawl(self, pub_date):
        pass # Comic no longer published
