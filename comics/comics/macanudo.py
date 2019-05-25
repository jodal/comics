# encoding: utf-8

from comics.aggregator.crawler import DagbladetCrawlerBase
from comics.core.comic_data import ComicDataBase


class ComicData(ComicDataBase):
    name = 'Macanudo'
    language = 'no'
    url = 'http://www.dagbladet.no/tegneserie/macanudo/'
    rights = 'Liniers'


class Crawler(DagbladetCrawlerBase):
    history_capable_days = 14
    schedule = 'Mo,Tu,We,Th,Fr'
    time_zone = 'Europe/Oslo'

    def crawl(self, pub_date):
        return self.crawl_helper('macanudo', pub_date)
