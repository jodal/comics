from comics.aggregator.crawler import CrawlerBase
from comics.core.comic_data import ComicDataBase


class ComicData(ComicDataBase):
    name = "Tommy og Tigern"
    language = "no"
    url = "http://heltnormalt.no/tommytigern"
    rights = "Bill Watterson"
    active = False


class Crawler(CrawlerBase):
    def crawl(self, pub_date):
        pass  # Comic no longer published
