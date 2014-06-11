from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.core.comic_data import ComicDataBase


class ComicData(ComicDataBase):
    name = 'Pink Parts'
    language = 'en'
    url = 'http://pinkpartscomic.com/'
    start_date = '2010-02-01'
    end_date = '2014-02-23'
    active = False
    rights = 'Katherine Skipper'


class Crawler(CrawlerBase):
    def crawl(self, pub_date):
        pass  # Comic no longer published
