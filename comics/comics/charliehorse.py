from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.meta.base import MetaBase

class Meta(MetaBase):
    name = 'Charliehorse'
    language = 'en'
    url = 'http://www.krakowstudios.com/'
    active = False
    start_date = '2009-01-01'
    end_date = '2010-02-27'
    rights = 'Iron Muse Media'

class Crawler(CrawlerBase):
    def crawl(self, pub_date):
        pass # Comic no longer published
