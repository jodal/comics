# encoding: utf-8

from comics.aggregator.crawler import HeltNormaltCrawlerBase
from comics.core.comic_data import ComicDataBase


class ComicData(ComicDataBase):
    name = 'Kollektivet'
    language = 'no'
    url = 'http://heltnormalt.no/kollektivet'
    rights = 'Torbjørn Lien'


class Crawler(HeltNormaltCrawlerBase):
    history_capable_date = '2013-05-01'
    schedule = 'Mo,Tu,We,Th,Fr,Sa'

    def crawl(self, pub_date):
        return self.crawl_helper('kollektivet', pub_date)
