from comics.aggregator.crawler import CrawlerBase
from comics.core.comic_data import ComicDataBase


class ComicData(ComicDataBase):
    name = "PartiallyClips"
    language = "en"
    url = "http://partiallyclips.com/"
    start_date = "2002-01-01"
    rights = "Robert T. Balder"
    active = False


class Crawler(CrawlerBase):
    def crawl(self, pub_date):
        pass
