from comics.aggregator.crawler import CrawlerBase
from comics.core.comic_data import ComicDataBase


class ComicData(ComicDataBase):
    name = "Hjalmar"
    language = "no"
    url = "http://heltnormalt.no/hjalmar"
    rights = "Nils Axle Kanten"
    active = False


class Crawler(CrawlerBase):
    def crawl(self, pub_date):
        pass  # Comic no longer published
