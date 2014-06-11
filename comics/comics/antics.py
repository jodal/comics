from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.core.comic_data import ComicDataBase


class ComicData(ComicDataBase):
    name = 'Antics'
    language = 'en'
    url = 'http://www.anticscomic.com/'
    start_date = '2008-10-25'
    end_date = '2013-12-24'
    active = False
    rights = 'Fletcher'


class Crawler(CrawlerBase):
    def crawl(self, pub_date):
        pass  # Comic no longer published
