import re

from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.core.comic_data import ComicDataBase


class ComicData(ComicDataBase):
    name = 'Eat That Toast!'
    language = 'en'
    url = 'http://eatthattoast.com/'
    start_date = '2010-06-14'
    end_date = '2013-12-02'
    active = False
    rights = 'Matt Czapiewski'


class Crawler(CrawlerBase):
    def crawl(self, pub_date):
        pass  # Comic no longer published
