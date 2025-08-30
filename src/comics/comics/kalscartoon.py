from comics.aggregator.crawler import CrawlerBase
from comics.core.comic_data import ComicDataBase


class ComicData(ComicDataBase):
    name = "KAL's Cartoon"
    language = "en"
    url = "http://www.economist.com/"
    start_date = "2006-01-05"
    rights = "Kevin Kallaugher"
    active = False


class Crawler(CrawlerBase):
    def crawl(self, pub_date):
        pass  # Comic no longer published
