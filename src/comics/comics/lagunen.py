from comics.aggregator.crawler import CrawlerBase
from comics.core.comic_data import ComicDataBase


class ComicData(ComicDataBase):
    name = "Lagunen"
    language = "no"
    url = "http://www.start.no/tegneserier/lagunen/"
    active = False
    start_date = "1991-05-13"
    rights = "Jim Toomey"


class Crawler(CrawlerBase):
    def crawl(self, pub_date):
        pass  # Comic no longer published
