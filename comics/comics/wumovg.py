from comics.aggregator.crawler import HeltNormaltCrawlerBase
from comics.core.comic_data import ComicDataBase


class ComicData(ComicDataBase):
    name = 'Wumo (vg.no)'
    language = 'no'
    url = 'http://heltnormalt.no/wumo'
    rights = 'Mikael Wulff & Anders Morgenthaler'


class Crawler(HeltNormaltCrawlerBase):
    history_capable_date = '2013-01-26'
    schedule = 'Mo,Tu,We,Th,Fr,Sa,Su'

    def crawl(self, pub_date):
        return self.crawl_helper('wumo', pub_date)
