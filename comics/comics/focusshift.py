from comics.aggregator.crawler import CrawlerBase
from comics.meta.base import MetaBase

class Meta(MetaBase):
    name = 'Focus Shift'
    language = 'en'
    url = 'http://www.osnews.com/comics/'
    start_date = '2008-01-27'
    history_capable_date = '2008-01-27'
    schedule = 'Mo,Tu,We,Th,Fr,Sa,Su'
    time_zone = 1
    rights = 'Thom Holwerda'

class Crawler(CrawlerBase):
    def crawl(self, pub_date):
        pass # Comic no longer published
