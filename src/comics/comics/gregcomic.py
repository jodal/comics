from comics.aggregator.crawler import CrawlerBase
from comics.core.comic_data import ComicDataBase


class ComicData(ComicDataBase):
    name = "Greg Comic"
    language = "en"
    url = "http://gregcomic.com/"
    start_date = "2011-06-01"
    end_date = "2013-12-20"
    active = False
    rights = "Chur Yin Wan"


class Crawler(CrawlerBase):
    def crawl(self, pub_date):
        pass  # Comic no longer published
