from comics.aggregator.crawler import CrawlerBase
from comics.core.comic_data import ComicDataBase


class ComicData(ComicDataBase):
    name = "Undeclared Major"
    language = "en"
    url = "http://www.undeclaredcomics.com/"
    start_date = "2011-08-09"
    end_date = "2012-09-11"
    active = False
    rights = "Belal"


class Crawler(CrawlerBase):
    def crawl(self, pub_date):
        pass  # Comic no longer published
