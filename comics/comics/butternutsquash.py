# encoding: utf-8

from comics.aggregator.crawler import CrawlerBase
from comics.core.comic_data import ComicDataBase


class ComicData(ComicDataBase):
    name = "Butternutsquash"
    language = "en"
    url = "http://www.butternutsquash.net/"
    active = False
    start_date = "2003-04-16"
    end_date = "2010-03-18"
    rights = "Ramón Pérez & Rob Coughler"


class Crawler(CrawlerBase):
    def crawl(self, pub_date):
        pass  # Comic no longer published
