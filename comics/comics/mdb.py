# encoding: utf-8

from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.meta.base import MetaBase

class Meta(MetaBase):
    name = 'M (db.no)'
    language = 'no'
    url = 'http://www.dagbladet.no/tegneserie/m'
    rights = 'Mads Eriksen'

class Crawler(CrawlerBase):
    history_capable_days = 14
    schedule = 'Mo,We,Fr'
    time_zone = 1

    def crawl(self, pub_date):
        url = 'http://www.dagbladet.no/tegneserie/markiv/serve.php?%s' % (
            self.date_to_epoch(pub_date),)
        return CrawlerImage(url)
