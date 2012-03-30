from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.core.comic_data import ComicDataBase

class ComicData(ComicDataBase):
    name = 'Billy'
    language = 'no'
    url = 'http://www.billy.no/'
    start_date = '1950-01-01'
    active = False
    rights = 'Mort Walker'

class Crawler(CrawlerBase):
    def crawl(self, pub_date):
        pass # Comic no longer published
