# encoding: utf-8

from comics.aggregator.crawler import CrawlerBase
from comics.core.comic_data import ComicDataBase


class ComicData(ComicDataBase):
    name = "Fakta fra verden"
    language = "no"
    url = "http://www.dagbladet.no/tegneserie/faktafraverden/"
    active = False
    start_date = "2001-01-01"
    rights = "Karstein Volle"


class Crawler(CrawlerBase):
    def crawl(self, pub_date):
        pass  # Comic no longer published
