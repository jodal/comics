from comics.aggregator.crawler import CrawlerBase
from comics.core.comic_data import ComicDataBase


class ComicData(ComicDataBase):
    name = "Wumo (vg.no)"
    language = "no"
    url = "http://heltnormalt.no/wumo"
    rights = "Mikael Wulff & Anders Morgenthaler"
    active = False


class Crawler(CrawlerBase):
    def crawl(self, pub_date):
        pass  # Comic no longer published
