from comics.aggregator.crawler import PondusNoCrawlerBase
from comics.meta.base import MetaBase

class Meta(MetaBase):
    name = 'Carpe Diem (pondus.no)'
    language = 'no'
    url = 'http://pondus.no/#CartoonGallery'
    rights = 'Nikklas Eriksson'

class Crawler(PondusNoCrawlerBase):
    history_capable_days = 14
    schedule = 'Mo,Tu,Th,Fr,Su'

    def crawl(self, pub_date):
        return self.crawl_helper('Carpe-Diem', pub_date)

