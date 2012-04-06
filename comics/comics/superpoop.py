from comics.aggregator.crawler import CrawlerBase
from comics.core.comic_data import ComicDataBase

class ComicData(ComicDataBase):
    name = 'Superpoop'
    language = 'en'
    url = 'http://www.superpoop.com/'
    active = False
    start_date = '2008-01-01'
    end_date = '2010-12-17'
    rights = 'Drew'

class Crawler(CrawlerBase):
    def crawl(self, pub_date):
        pass # Comic no longer published
