from comics.aggregator.crawler import CrawlerBase
from comics.core.comic_data import ComicDataBase


class ComicData(ComicDataBase):
    name = 'Orneryboy'
    language = 'en'
    url = 'http://www.orneryboy.com/'
    start_date = '2002-07-22'
    end_date = '2012-04-16'
    active = False
    rights = 'Michael Lalonde'


class Crawler(CrawlerBase):
    def crawl(self, pub_date):
        pass  # Comic no longer published
