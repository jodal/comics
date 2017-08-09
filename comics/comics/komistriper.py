# encoding: utf-8

from comics.aggregator.crawler import NettserierCrawlerBase
from comics.core.comic_data import ComicDataBase


class ComicData(ComicDataBase):
    name = 'Komistriper'
    language = 'no'
    url = 'http://aikomi.nettserier.no/'
    rights = 'Emil Åslund'
    start_date = '2015-01-14'


class Crawler(NettserierCrawlerBase):
    history_capable_date = '2015-01-14'
    time_zone = 'Europe/Oslo'

    def crawl(self, pub_date):
        return self.crawl_helper('aikomi', pub_date)
