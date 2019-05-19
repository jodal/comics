from comics.aggregator.crawler import DagbladetCrawlerBase
from comics.core.comic_data import ComicDataBase


class ComicData(ComicDataBase):
    name = 'Rocky (db.no)'
    language = 'no'
    url = 'http://www.dagbladet.no/tegneserie/rocky/'
    start_date = '1998-01-01'
    end_date = '2018-07-14'
    active = False
    rights = 'Martin Kellerman'


class Crawler(DagbladetCrawlerBase):
    def crawl(self, pub_date):
        pass  # Comic no longer published
