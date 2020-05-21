from comics.aggregator.crawler import CrawlerBase
from comics.core.comic_data import ComicDataBase


class ComicData(ComicDataBase):
    name = "Dilbert (vg.no)"
    language = "no"
    url = "http://heltnormalt.no/dilbert"
    start_date = "1989-04-16"
    rights = "Scott Adams"
    active = False


class Crawler(CrawlerBase):
    def crawl(self, pub_date):
        pass  # Comic no longer published
