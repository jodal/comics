# noqa: N999

from comics.aggregator.crawler import CrawlerBase
from comics.core.comic_data import ComicDataBase


class ComicData(ComicDataBase):
    name = "8-Bit Theater"
    language = "en"
    url = "http://www.nuklearpower.com/"
    active = False
    start_date = "2001-03-02"
    end_date = "2010-06-01"
    rights = "Brian Clevinger"


class Crawler(CrawlerBase):
    def crawl(self, pub_date):
        pass  # Comic no longer published
