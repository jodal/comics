# encoding: utf-8

from comics.aggregator.crawler import CrawlerBase
from comics.core.comic_data import ComicDataBase


class ComicData(ComicDataBase):
    name = 'Lunch'
    language = 'no'
    url = 'http://lunchstriper.lunddesign.no/'
    start_date = '2009-10-21'
    active = False
    rights = 'Børge Lund'


class Crawler(CrawlerBase):
    def crawl(self, pub_date):
        pass  # Comic no longer published at this site
