from comics.aggregator.crawler import CrawlerBase
from comics.core.comic_data import ComicDataBase


class ComicData(ComicDataBase):
    name = "Kukuburi"
    language = "en"
    url = "http://www.kukuburi.com/"
    start_date = "2007-09-08"
    end_date = "2012-01-11"
    active = False
    rights = "Ramón Pérez"


class Crawler(CrawlerBase):
    def crawl(self, pub_date):
        pass  # Comic no longer published
