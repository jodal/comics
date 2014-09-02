# encoding: utf-8

from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.core.comic_data import ComicDataBase


class ComicData(ComicDataBase):
    name = 'Walk of Life'
    language = 'no'
    url = 'http://walkoflife.nettserier.no/'
    start_date = '2008-06-23'
    end_date = '2014-06-24'
    active = False
    rights = 'Trond J. Stavås'


class Crawler(CrawlerBase):
    def crawl(self, pub_date):
        pass  # Comic no longer published
