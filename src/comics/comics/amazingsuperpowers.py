from comics.aggregator.crawler import CrawlerBase
from comics.core.comic_data import ComicDataBase


class ComicData(ComicDataBase):
    name = "AmazingSuperPowers"
    language = "en"
    url = "http://www.amazingsuperpowers.com/"
    start_date = "2007-09-24"
    rights = "Wes & Tony"
    active = False


class Crawler(CrawlerBase):
    def crawl(self, pub_date):
        pass  # Comic no longer published
