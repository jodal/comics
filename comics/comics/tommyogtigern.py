from comics.aggregator.crawler import HeltNormaltCrawlerBase
from comics.core.comic_data import ComicDataBase


class ComicData(ComicDataBase):
    name = 'Tommy og Tigern'
    language = 'no'
    url = 'http://heltnormalt.no/tommytigern'
    rights = 'Bill Watterson'


class Crawler(HeltNormaltCrawlerBase):
    history_capable_date = '2013-02-01'
    schedule = 'Mo,Tu,We,Th,Fr,Sa,Su'

    def crawl(self, pub_date):
        return self.crawl_helper('tommytigern', pub_date)
