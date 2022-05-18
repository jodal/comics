from comics.aggregator.crawler import CrawlerBase
from comics.core.comic_data import ComicDataBase


class ComicData(ComicDataBase):
    name = "Lunch (e24.no)"
    language = "no"
    url = "http://www.e24.no/lunch/"
    start_date = "2009-10-21"
    rights = "Børge Lund"
    active = False


class Crawler(CrawlerBase):
    time_zone = "Europe/Oslo"

    def crawl(self, pub_date):
        pass
