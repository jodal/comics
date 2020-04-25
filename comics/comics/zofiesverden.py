from comics.aggregator.crawler import CrawlerBase
from comics.core.comic_data import ComicDataBase


class ComicData(ComicDataBase):
    name = "Zofies verden"
    language = "no"
    url = "http://www.zofiesverden.no/"
    start_date = "2006-05-02"
    end_date = "2012-08-31"
    active = False
    rights = "Grethe Nestor & Norunn Blichfeldt Schjerven"


class Crawler(CrawlerBase):
    def crawl(self, pub_date):
        pass  # Comic no longer published
