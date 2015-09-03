from comics.aggregator.crawler import HeltNormaltCrawlerBase
from comics.core.comic_data import ComicDataBase


class ComicData(ComicDataBase):
    name = 'Dilbert (vg.no)'
    language = 'no'
    url = 'http://heltnormalt.no/dilbert'
    start_date = '1989-04-16'
    rights = 'Scott Adams'


class Crawler(HeltNormaltCrawlerBase):
    history_capable_date = '2013-02-01'
    schedule = 'Mo,Tu,We,Th,Fr,Sa,Su'

    def crawl(self, pub_date):
        return self.crawl_helper('dilbert', pub_date)
