# encoding: utf-8

from comics.aggregator.crawler import PondusNoCrawlerBase
from comics.comics.pondus import Meta as PondusMeta

class Meta(PondusMeta):
    name = 'Pondus (pondus.no)'
    url = 'http://www.pondus.no/'
    active = False

class Crawler(PondusNoCrawlerBase):
    def crawl(self, pub_date):
        pass # Comic no longer published
