# encoding: utf-8

from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.meta.base import MetaBase

class Meta(MetaBase):
    name = 'Pondus (db.no)'
    language = 'no'
    url = 'http://www.dagbladet.no/tegneserie/pondus/'
    start_date = '1995-01-01'
    rights = 'Frode Øverli'

class Crawler(CrawlerBase):
    history_capable_days = 14
    schedule = 'Mo,Tu,We,Th,Fr,Sa,Su'
    time_zone = 1

    def crawl(self, pub_date):
        url = 'http://www.dagbladet.no/tegneserie/pondusarkiv/serve.php?%s' % (
            self.date_to_epoch(pub_date),)
        return CrawlerImage(url)
