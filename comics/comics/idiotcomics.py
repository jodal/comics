from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.meta.base import MetaBase

class Meta(MetaBase):
    name = 'Idiot Comics'
    language = 'en'
    url = 'http://www.idiotcomics.com/'
    start_date = '2006-09-08'
    end_date = '2010-02-15'
    rights = 'Robert Sergel'

class Crawler(CrawlerBase):
    history_capable_days = 500
    schedule = None
    time_zone = -5

    def crawl(self, pub_date):
        pass # Comic no longer published
