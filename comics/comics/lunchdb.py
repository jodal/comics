# encoding: utf-8

from comics.aggregator.crawler import DagbladetCrawlerBase
from comics.core.comic_data import ComicDataBase


class ComicData(ComicDataBase):
    name = 'Lunch (db.no)'
    language = 'no'
    url = 'http://www.dagbladet.no/tegneserie/lunch/'
    start_date = '2009-10-21'
    active = False
    rights = 'Børge Lund'


class Crawler(DagbladetCrawlerBase):
    history_capable_days = 14
    schedule = 'Mo,Tu,We,Th,Fr,Sa'
    time_zone = 'Europe/Oslo'

    def crawl(self, pub_date):
        pass  # Comic no longer published on this site
