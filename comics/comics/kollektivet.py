# encoding: utf-8

from comics.aggregator.crawler import CrawlerBase
from comics.core.comic_data import ComicDataBase


class ComicData(ComicDataBase):
    name = "Kollektivet"
    language = "no"
    url = "http://heltnormalt.no/kollektivet"
    rights = "Torbjørn Lien"
    active = False


class Crawler(CrawlerBase):
    def crawl(self, pub_date):
        pass  # Comic no longer published
