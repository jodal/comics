from comics.aggregator.crawler import HeltNormaltCrawlerBase
from comics.core.comic_data import ComicDataBase


class ComicData(ComicDataBase):
    name = 'Hjalmar'
    language = 'no'
    url = 'http://heltnormalt.no/hjalmar'
    rights = 'Nils Axle Kanten'


class Crawler(HeltNormaltCrawlerBase):
    history_capable_date = '2013-01-15'
    schedule = 'Mo,Tu,We,Th,Fr,Sa,Su'

    def crawl(self, pub_date):
        return self.crawler_helper('hjalmar', pub_date)
