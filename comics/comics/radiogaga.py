# encoding: utf-8

from comics.aggregator.crawler import PondusNoCrawlerBase
from comics.core.comic_data import ComicDataBase


class ComicData(ComicDataBase):
    name = 'Radio Gaga (pondus.no)'
    language = 'no'
    url = 'http://www.pondus.no/'
    rights = 'Øyvind Sagåsen'
    active = False


class Crawler(PondusNoCrawlerBase):
    def crawl(self, pub_date):
        pass  # Comic no longer published
