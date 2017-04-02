# encoding: utf-8

from comics.aggregator.crawler import DagbladetCrawlerBase
from comics.core.comic_data import ComicDataBase


class ComicData(ComicDataBase):
    name = 'Pondus (db.no)'
    language = 'no'
    url = 'http://www.dagbladet.no/tegneserie/pondus/'
    start_date = '1995-01-01'
    rights = 'Frode Øverli'


class Crawler(DagbladetCrawlerBase):
    history_capable_days = 14
    schedule = 'Mo,Tu,We,Th,Fr,Sa'
    time_zone = 'Europe/Oslo'

    def crawl(self, pub_date):
        return self.crawl_helper('pondus',pub_date)
