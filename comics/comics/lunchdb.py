# encoding: utf-8

from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.meta.base import MetaBase

class Meta(MetaBase):
    name = 'Lunch (db.no)'
    language = 'no'
    url = 'http://www.dagbladet.no/tegneserie/lunch/'
    start_date = '2009-10-21'
    rights = 'Børge Lund'

class Crawler(CrawlerBase):
    history_capable_days = 14
    schedule = 'Tu,Th,Sa'
    time_zone = 1

    def crawl(self, pub_date):
        url = 'http://www.dagbladet.no/tegneserie/luncharkiv/serve.php?%s' % (
            self.date_to_epoch(pub_date),)
        return CrawlerImage(url)
