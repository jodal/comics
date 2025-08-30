from comics.aggregator.crawler import CrawlerBase
from comics.core.comic_data import ComicDataBase


class ComicData(ComicDataBase):
    name = "Abstruse Goose"
    language = "en"
    start_date = "2008-02-01"
    rights = "lcfr, CC BY-NC 3.0 US"
    active = False


class Crawler(CrawlerBase):
    def crawl(self, pub_date):
        pass  # Comic no longer published
