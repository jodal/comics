# encoding: utf-8

from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.meta.base import MetaBase

class Meta(MetaBase):
    name = 'Rutetid'
    language = 'no'
    url = 'http://www.dagbladet.no/tegneserie/rutetid/'
    rights = 'Frode Øverli'

class Crawler(CrawlerBase):
    history_capable_days = 15
    schedule = 'Fr,Sa,Su'
    time_zone = 1

    def crawl(self, pub_date):
        url = 'http://www.dagbladet.no/tegneserie/rutetidarkiv/serve.php?%s' % (
            self.date_to_epoch(pub_date),)
        return CrawlerImage(url)
