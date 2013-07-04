from comics.aggregator.crawler import PondusNoCrawlerBase
from comics.core.comic_data import ComicDataBase


class ComicData(ComicDataBase):
    name = 'Carpe Diem (pondus.no)'
    language = 'no'
    url = 'http://www.pondus.no/'
    rights = 'Nikklas Eriksson'
    active = False


class Crawler(PondusNoCrawlerBase):
    def crawl(self, pub_date):
        pass  # Comic no longer published
