from comics.aggregator.crawler import CrawlerBase
from comics.core.comic_data import ComicDataBase


class ComicData(ComicDataBase):
    name = "Life With Rippy"
    language = "en"
    url = "http://www.rhymes-with-witch.com/"
    active = False
    start_date = "2006-08-09"
    end_date = "2009-11-25"
    rights = "r*k*milholland"


class Crawler(CrawlerBase):
    def crawl(self, pub_date):
        pass  # Comic no longer published
