# encoding: utf-8

from comics.aggregator.crawler import CrawlerBase
from comics.core.comic_data import ComicDataBase


class ComicData(ComicDataBase):
    name = 'Havet'
    language = 'no'
    url = 'http://havet.nettserier.no/'
    start_date = '2007-09-27'
    end_date = '2012-10-25'
    active = False
    rights = 'Øystein Ottesen'


class Crawler(CrawlerBase):
    def crawl(self, pub_date):
        pass  # Comic no longer published
