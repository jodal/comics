from comics.aggregator.crawler import CrawlerBase
from comics.core.comic_data import ComicDataBase


class ComicData(ComicDataBase):
    name = 'Overcompensating'
    language = 'en'
    url = 'http://www.overcompensating.com/'
    start_date = '2004-09-29'
    active = False
    rights = 'Jeff Rowland'


class Crawler(CrawlerBase):
    def crawl(self, pub_date):
        pass  # Comic no longer published
