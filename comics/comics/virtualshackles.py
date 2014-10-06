import re

from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.core.comic_data import ComicDataBase


class ComicData(ComicDataBase):
    name = 'Virtual Shackles'
    language = 'en'
    url = 'http://www.virtualshackles.com/'
    start_date = '2009-03-27'
    end_date = '2014-02-15'
    active = False
    rights = 'Jeremy Vinar & Mike Fahmie'


class Crawler(CrawlerBase):
    def crawl(self, pub_date):
        pass  # Comic no longer published
