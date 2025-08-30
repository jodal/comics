from comics.aggregator.crawler import CrawlerBase
from comics.core.comic_data import ComicDataBase


class ComicData(ComicDataBase):
    name = "A Softer World"
    language = "en"
    url = "http://www.asofterworld.com/"
    start_date = "2003-02-07"
    end_date = "2015-10-30"
    rights = "Joey Comeau, Emily Horne"
    active = False


class Crawler(CrawlerBase):
    schedule = None
    time_zone = "America/Los_Angeles"

    def crawl(self, pub_date):
        pass  # Comic no longer published
