# encoding: utf-8

from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.meta.base import MetaBase

class Meta(MetaBase):
    name = 'Rutetid'
    language = 'no'
    url = 'http://www.dagbladet.no/tegneserie/rutetid/'
    rights = 'Frode Øverli'

class Crawler(CrawlerBase):
    def crawl(self, pub_date):
        pass # Comic no longer published
