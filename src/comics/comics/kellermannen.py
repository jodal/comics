from comics.aggregator.crawler import CrawlerBase
from comics.core.comic_data import ComicDataBase


class ComicData(ComicDataBase):
    name = "Kellermannen"
    language = "no"
    url = "http://www.dagbladet.no/tegneserie/kellermannen/"
    rights = "Martin Kellerman"
    active = False


class Crawler(CrawlerBase):
    history_capable_days = 30
    time_zone = "Europe/Oslo"

    def crawl(self, pub_date):
        pass  # Comic no longer published
