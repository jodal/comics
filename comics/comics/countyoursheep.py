from comics.aggregator.crawler import CrawlerBase
from comics.core.comic_data import ComicDataBase


class ComicData(ComicDataBase):
    name = 'Count Your Sheep'
    language = 'en'
    url = 'http://www.countyoursheep.com/'
    start_date = '2003-06-11'
    end_date = '2011-12-07'
    active = False
    rights = 'Adrian "Adis" Ramos'


class Crawler(CrawlerBase):
    def crawl(self, pub_date):
        pass  # Comic no longer published
