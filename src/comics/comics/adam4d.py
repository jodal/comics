from comics.aggregator.crawler import CrawlerBase
from comics.core.comic_data import ComicDataBase


class ComicData(ComicDataBase):
    name = "Adam4d.com"
    url = "https://www.adam4d.com/"
    language = "en"
    start_date = "2012-07-03"
    rights = "Adam Ford"
    active = False


class Crawler(CrawlerBase):
    def crawl(self, pub_date):
        pass  # Comic no longer published
