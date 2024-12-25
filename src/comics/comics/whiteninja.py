from comics.aggregator.crawler import CrawlerBase
from comics.core.comic_data import ComicDataBase


class ComicData(ComicDataBase):
    name = "White Ninja"
    language = "en"
    url = "http://www.whiteninjacomics.com/"
    start_date = "2002-01-01"
    end_date = "2012-08-04"
    active = False
    rights = "Scott Bevan & Kent Earle"


class Crawler(CrawlerBase):
    def crawl(self, pub_date):
        pass  # Comic no longer published
