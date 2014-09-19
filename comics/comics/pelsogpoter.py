from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.core.comic_data import ComicDataBase


class ComicData(ComicDataBase):
    name = 'Pels og Poter'
    language = 'no'
    url = 'http://www.start.no/tegneserier/'
    start_date = '1994-01-01'
    active = False
    rights = 'Patrick McDonnell'


class Crawler(CrawlerBase):
    def crawl(self, pub_date):
        pass  # Comic no longer published
