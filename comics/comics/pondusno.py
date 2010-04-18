# encoding: utf-8

from comics.aggregator.crawler import PondusNoCrawlerBase
from comics.comics.pondus import Meta as PondusMeta

class Meta(PondusMeta):
    name = 'Pondus (pondus.no)'
    url = 'http://pondus.no/Tegneserier/Pondusstriper/'

class Crawler(PondusNoCrawlerBase):
    schedule = 'Su'
    history_capable_days = 7 * 10 # weeks

    def crawl(self, pub_date):
        return self.crawl_helper('Pondus', pub_date)

