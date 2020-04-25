from comics.aggregator.crawler import PondusNoCrawlerBase
from comics.core.comic_data import ComicDataBase


class ComicData(ComicDataBase):
    name = "Helt Nils"
    language = "no"
    url = "http://www.pondus.no/"
    active = False
    rights = "Nils Ofstad"


class Crawler(PondusNoCrawlerBase):
    def crawl(self, pub_date):
        pass  # Comic no longer published
