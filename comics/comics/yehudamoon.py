from comics.aggregator.crawler import CrawlerBase
from comics.core.comic_data import ComicDataBase


class ComicData(ComicDataBase):
    name = 'Yehuda Moon'
    language = 'en'
    url = 'http://www.yehudamoon.com/'
    start_date = '2008-01-22'
    end_date = '2012-12-31'
    active = False
    rights = 'Rick Smith'


class Crawler(CrawlerBase):
    def crawl(self, pub_date):
        pass  # Comic no longer published
