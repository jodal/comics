from comics.aggregator.crawler import DagbladetCrawlerBase
from comics.core.comic_data import ComicDataBase


class ComicData(ComicDataBase):
    name = "Pondus (db.no)"
    language = "no"
    url = "https://www.dagbladet.no/tegneserie/pondus/"
    start_date = "1995-01-01"
    active = False
    rights = "Frode Øverli"


class Crawler(DagbladetCrawlerBase):
    def crawl(self, pub_date):
        pass  # Comic no longer published on this site
