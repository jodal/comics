from comics.aggregator.crawler import DagbladetCrawlerBase
from comics.core.comic_data import ComicDataBase


class ComicData(ComicDataBase):
    name = 'Zelda'
    language = 'no'
    url = 'http://www.dagbladet.no/tegneserie/zelda-lille-berlin/'
    start_date = '2012-06-07'
    rights = 'Lina Neidestam'
    active = False


class Crawler(DagbladetCrawlerBase):
    def crawl(self, pub_date):
        pass   # Comic no longer published
