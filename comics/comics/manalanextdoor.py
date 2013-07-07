from comics.aggregator.crawler import CrawlerBase
from comics.core.comic_data import ComicDataBase


class ComicData(ComicDataBase):
    name = 'Manala Next Door'
    language = 'en'
    url = 'http://www.manalanextdoor.com/'
    start_date = '2011-01-23'
    end_date = '2012-11-14'
    active = False
    rights = 'Humon'


class Crawler(CrawlerBase):
    def crawl(self, pub_date):
        pass  # Comic no longer published
