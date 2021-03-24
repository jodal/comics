from comics.aggregator.crawler import PondusNoCrawlerBase
from comics.comics.pondus import ComicData as PondusData


class ComicData(PondusData):
    name = "Pondus (pondus.no)"
    url = "http://www.pondus.no/"
    active = False


class Crawler(PondusNoCrawlerBase):
    def crawl(self, pub_date):
        pass  # Comic no longer published
