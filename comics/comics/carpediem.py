from comics.aggregator.crawler import PondusNoCrawlerBase
from comics.core.comic_data import ComicDataBase

class ComicData(ComicDataBase):
    name = 'Carpe Diem (pondus.no)'
    language = 'no'
    url = 'http://www.pondus.no/'
    rights = 'Nikklas Eriksson'

class Crawler(PondusNoCrawlerBase):
    schedule = 'Mo,Tu,Th,Fr,Su'

    def crawl(self, pub_date):
        return self.crawl_helper('20056')
