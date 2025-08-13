from comics.aggregator.crawler import NettserierCrawlerBase
from comics.core.comic_data import ComicDataBase


class ComicData(ComicDataBase):
    name = "Wyyrd"
    language = "no"
    url = "http://wyyrd.nettserier.no/"
    active = False
    start_date = "2008-01-14"
    end_date = "2020-11-01"
    rights = "Gard Robot Helset"


class Crawler(NettserierCrawlerBase):
    history_capable_date = "2008-01-14"
    time_zone = "Europe/Oslo"

    def crawl(self, pub_date):
        pass  # Comic no longer published
