# encoding: utf-8

from comics.aggregator.crawler import CrawlerBase, CrawlerResult
from comics.meta.base import MetaBase

class Meta(MetaBase):
    name = 'Rutetid'
    language = 'no'
    url = 'http://www.dagbladet.no/tegneserie/rutetid/'
    history_capable_days = 15
    schedule = 'Fr,Sa,Su'
    time_zone = 1
    rights = 'Frode Øverli'

class Crawler(CrawlerBase):
    def crawl(self, pub_date):
        url = 'http://www.dagbladet.no/tegneserie/rutetidarkiv/serve.php?%(date)s' % {
            'date': self.date_to_epoch(pub_date),
        }
        return CrawlerResult(url)
