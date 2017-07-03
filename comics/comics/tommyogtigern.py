from comics.aggregator.crawler import HeltNormaltCrawlerBase
from comics.core.comic_data import ComicDataBase


class ComicData(ComicDataBase):
    name = 'Tommy og Tigern'
    language = 'no'
    url = 'http://heltnormalt.no/tommytigern'
    rights = 'Bill Watterson'
    active = False


class Crawler(HeltNormaltCrawlerBase):
    history_capable_date = '2013-02-01'

    def crawl(self, pub_date):
        pass  # Comic no longer published
