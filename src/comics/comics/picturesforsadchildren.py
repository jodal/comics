from comics.aggregator.crawler import CrawlerBase
from comics.core.comic_data import ComicDataBase


class ComicData(ComicDataBase):
    name = "pictures for sad children"
    language = "en"
    url = "http://picturesforsadchildren.com/"
    start_date = "2007-01-01"
    end_date = "2012-11-26"
    active = False
    rights = "John Campbell"


class Crawler(CrawlerBase):
    def crawl(self, pub_date):
        pass  # Comic no longer published
