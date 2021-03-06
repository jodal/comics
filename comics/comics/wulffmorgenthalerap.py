from comics.aggregator.crawler import CrawlerBase
from comics.core.comic_data import ComicDataBase


class ComicData(ComicDataBase):
    name = "Wumo (ap.no)"
    language = "no"
    url = "http://www.aftenposten.no/tegneserier/"
    start_date = "2001-01-01"
    active = False
    rights = "Mikael Wulff & Anders Morgenthaler"


class Crawler(CrawlerBase):
    def crawl(self, pub_date):
        pass  # Comic no longer published
