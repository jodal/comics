from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.core.comic_data import ComicDataBase


class ComicData(ComicDataBase):
    name = 'The Idle State'
    language = 'en'
    url = 'http://www.theidlestate.com/'
    start_date = '2011-07-18'
    end_date = '2012-07-05'
    active = False
    rights = 'Nick Wright'


class Crawler(CrawlerBase):
    def crawl(self, pub_date):
        pass  # Comic no longer published
