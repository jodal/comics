from comics.aggregator.crawler import CrawlerBase
from comics.core.comic_data import ComicDataBase


class ComicData(ComicDataBase):
    name = "Treading Ground"
    language = "en"
    url = "http://www.treadingground.com/"
    active = False
    start_date = "2003-10-12"
    rights = "Nick Wright"


class Crawler(CrawlerBase):
    def crawl(self, pub_date):
        pass  # Comic no longer published
