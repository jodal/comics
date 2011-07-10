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
    def crawl(self, pub_date):
        pass # Comic no longer published
