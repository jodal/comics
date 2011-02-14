from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.meta.base import MetaBase

class Meta(MetaBase):
    name = 'Charliehorse'
    language = 'en'
    url = 'http://www.krakowstudios.com/'
    start_date = '2009-01-01'
    end_date = '2010-02-27'
    rights = 'Iron Muse Media'

class Crawler(CrawlerBase):
    history_capable_date = '2009-01-01'
    schedule = None
    time_zone = -5

    def crawl(self, pub_date):
        pass # Comic no longer published
