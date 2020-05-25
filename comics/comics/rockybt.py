from comics.aggregator.crawler import CrawlerBase
from comics.comics.rocky import ComicData as RockyData


class ComicData(RockyData):
    name = "Rocky (bt.no)"
    url = "https://www.bt.no/kultur/tegneserier/"
    active = False


class Crawler(CrawlerBase):
    def crawl(self, pub_date):
        pass
