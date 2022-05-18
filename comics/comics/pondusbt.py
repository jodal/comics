from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.comics.pondus import ComicData as PondusData


class ComicData(PondusData):
    name = "Pondus (bt.no)"
    url = "https://www.bt.no/kultur/tegneserier/"
    active = False


class Crawler(CrawlerBase):
    time_zone = "Europe/Oslo"

    def crawl(self, pub_date):
        pass
