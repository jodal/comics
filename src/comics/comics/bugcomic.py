from comics.aggregator.crawler import CrawlerBase
from comics.core.comic_data import ComicDataBase


class ComicData(ComicDataBase):
    name = "Bug Martini"
    language = "en"
    url = "http://www.bugmartini.com/"
    start_date = "2009-10-19"
    rights = "Adam Huber"
    active = False


class Crawler(CrawlerBase):
    def crawl(self, pub_date):
        pass  # Comic no longer published
