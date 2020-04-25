from comics.aggregator.crawler import CrawlerBase
from comics.core.comic_data import ComicDataBase


class ComicData(ComicDataBase):
    name = "AppleGeeks"
    language = "en"
    url = "http://www.applegeeks.com/"
    start_date = "2003-01-01"
    end_date = "2010-11-22"
    active = False
    rights = "Mohammad Haque & Ananth Panagariya"


class Crawler(CrawlerBase):
    def crawl(self, pub_date):
        pass  # Comic no longer published
