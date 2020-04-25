from comics.aggregator.crawler import CrawlerBase
from comics.core.comic_data import ComicDataBase


class ComicData(ComicDataBase):
    name = "Dilbert (bt.no)"
    language = "no"
    url = "http://www.bt.no/tegneserier/dilbert/"
    active = False
    start_date = "1989-04-16"
    rights = "Scott Adams"


class Crawler(CrawlerBase):
    def crawl(self, pub_date):
        pass  # Comic no longer published
