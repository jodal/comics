from comics.aggregator.crawler import CrawlerBase
from comics.core.comic_data import ComicDataBase


class ComicData(ComicDataBase):
    name = 'AppleGeeks Lite'
    language = 'en'
    url = 'http://www.applegeeks.com/'
    start_date = '2006-04-18'
    end_date = '2010-08-30'
    active = False
    rights = 'Mohammad Haque & Ananth Panagariya'


class Crawler(CrawlerBase):
    def crawl(self, pub_date):
        pass  # Comic no longer published
