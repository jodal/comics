# encoding: utf-8

from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.meta.base import MetaBase

class Meta(MetaBase):
    name = 'Butternutsquash'
    language = 'en'
    url = 'http://www.butternutsquash.net/'
    start_date = '2003-04-16'
    end_date = '2010-03-18'
    rights = 'Ramón Pérez & Rob Coughler'

class Crawler(CrawlerBase):
    schedule = None

    def crawl(self, pub_date):
        pass # Comic no longer published
