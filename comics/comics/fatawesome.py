from comics.aggregator.crawler import CrawlerBase
from comics.core.comic_data import ComicDataBase


class ComicData(ComicDataBase):
    name = "Fatawesome"
    language = "en"
    url = "http://www.fatawesome.com/"
    start_date = "2014-09-16"
    rights = "James Craig"
    active = False


class Crawler(CrawlerBase):
    def crawl(self, pub_date):
        pass
