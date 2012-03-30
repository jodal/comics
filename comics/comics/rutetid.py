# encoding: utf-8

from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.core.comic_data import ComicDataBase

class ComicData(ComicDataBase):
    name = 'Rutetid'
    language = 'no'
    url = 'http://www.dagbladet.no/tegneserie/rutetid/'
    active = False
    rights = 'Frode Øverli'

class Crawler(CrawlerBase):
    def crawl(self, pub_date):
        pass # Comic no longer published
