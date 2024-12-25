from comics.aggregator.crawler import PondusNoCrawlerBase
from comics.core.comic_data import ComicDataBase


class ComicData(ComicDataBase):
    name = "EON"
    language = "no"
    url = "http://www.pondus.no/"
    start_date = "2008-11-19"
    active = False
    rights = "Lars Lauvik"


class Crawler(PondusNoCrawlerBase):
    def crawl(self, pub_date):
        pass  # Comic no longer published
