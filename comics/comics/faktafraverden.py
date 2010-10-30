# encoding: utf-8

from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.meta.base import MetaBase

class Meta(MetaBase):
    name = 'Fakta fra verden'
    language = 'no'
    url = 'http://www.dagbladet.no/tegneserie/faktafraverden/'
    start_date = '2001-01-01'
    rights = 'Karstein Volle'

class Crawler(CrawlerBase):
    history_capable_days = 40
    schedule = 'Mo,We,Fr'
    time_zone = 1

    def crawl(self, pub_date):
        url = 'http://www.dagbladet.no/tegneserie/faktafraverdenarkiv' \
            + '/serve.php?%s' % (self.date_to_epoch(pub_date),)
        return CrawlerImage(url)
