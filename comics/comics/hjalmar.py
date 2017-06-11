from comics.aggregator.crawler import HeltNormaltCrawlerBase
from comics.core.comic_data import ComicDataBase


class ComicData(ComicDataBase):
    name = 'Hjalmar'
    language = 'no'
    url = 'http://heltnormalt.no/hjalmar'
    rights = 'Nils Axle Kanten'
    active = False


class Crawler(HeltNormaltCrawlerBase):
    history_capable_date = '2013-01-15'

    def crawl(self, pub_date):
        pass  # Comic no longer published
