# encoding: utf-8

from comics.aggregator.crawler import CrawlerBase
from comics.core.comic_data import ComicDataBase


class ComicData(ComicDataBase):
    name = 'Uten Sokker'
    language = 'no'
    url = 'http://utensokker.nettserier.no/'
    start_date = '2009-07-14'
    start_date = '2012-02-02'
    active = False
    rights = 'Bjørnar Grandalen'


class Crawler(CrawlerBase):
    def crawl(self, pub_date):
        pass  # Comic no longer published
