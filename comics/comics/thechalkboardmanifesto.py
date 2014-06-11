from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.core.comic_data import ComicDataBase


class ComicData(ComicDataBase):
    name = 'The Chalkboard Manifesto'
    language = 'en'
    url = 'http://www.chalkboardmanifesto.com/'
    start_date = '2005-05-01'
    end_date = '2013-08-26'
    active = False
    rights = 'Shawn McDonald'


class Crawler(CrawlerBase):
    def crawl(self, pub_date):
        pass  # Comic no longer published
