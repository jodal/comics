from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.core.comic_data import ComicDataBase


class ComicData(ComicDataBase):
    name = "Nemi (bt.no)"
    language = "no"
    url = "https://www.bt.no/kultur/tegneserier/"
    start_date = "1997-01-01"
    rights = "Lise Myhre"
    active = False


class Crawler(CrawlerBase):
    time_zone = "Europe/Oslo"

    def crawl(self, pub_date):
        pass
