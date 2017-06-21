from comics.aggregator.crawler import HeltNormaltCrawlerBase
from comics.core.comic_data import ComicDataBase


class ComicData(ComicDataBase):
    name = 'Truth Facts'
    language = 'no'
    url = 'http://heltnormalt.no/truthfacts'
    active = False


class Crawler(HeltNormaltCrawlerBase):
    history_capable_date = '2013-02-12'
    schedule = 'Mo,Tu,We,Th,Fr'

    def crawl(self, pub_date):
        pass  # Comic no longer published
