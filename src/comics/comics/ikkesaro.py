from comics.aggregator.crawler import NettserierCrawlerBase
from comics.core.comic_data import ComicDataBase


class ComicData(ComicDataBase):
    name = "Ikke Saro"
    language = "no"
    url = "https://nettserier.no/ikkesaro/"
    rights = "Ladder"
    active = False
    start_date = "2016-06-16"
    end_date = "2019-10-31"


class Crawler(NettserierCrawlerBase):
    history_capable_date = "2016-06-16"
    time_zone = "Europe/Oslo"

    def crawl(self, pub_date):
        pass  # Comic no longer published
