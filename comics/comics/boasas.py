from comics.aggregator.crawler import CrawlerBase
from comics.core.comic_data import ComicDataBase


class ComicData(ComicDataBase):
    name = "Boy on a Stick and Slither"
    language = "en"
    url = "http://www.boasas.com/"
    start_date = "1998-01-01"
    end_date = "2011-09-12"
    active = False
    rights = "Steven L. Cloud"


class Crawler(CrawlerBase):
    def crawl(self, pub_date):
        pass  # Comic no longer published
