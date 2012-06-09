from comics.aggregator.crawler import PondusNoCrawlerBase
from comics.meta.base import MetaBase

class Meta(MetaBase):
    name = 'Carpe Diem (pondus.no)'
    language = 'no'
    url = 'http://www.pondus.no/'
    rights = 'Nikklas Eriksson'
    active = False

class Crawler(PondusNoCrawlerBase):
    def crawl(self, pub_date):
        pass # Comic no longer published
