from comics.aggregator.crawler import CrawlerBase
from comics.core.comic_data import ComicDataBase


class ComicData(ComicDataBase):
    name = 'Boxer Hockey'
    language = 'en'
    url = 'http://boxerhockey.fireball20xl.com/'
    start_date = '2007-11-25'
    end_date = '2013-08-03'
    active = False
    rights = 'Tyson "Rittz" Hesse'


class Crawler(CrawlerBase):
    def crawl(self, pub_date):
        pass  # Comic no longer published
