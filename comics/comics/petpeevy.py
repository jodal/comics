from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.core.comic_data import ComicDataBase

class ComicData(ComicDataBase):
    name = 'Pet Peevy'
    language = 'en'
    url = 'http://dobbcomics.com/'
    active = False
    rights = 'Rob Snyder'

class Crawler(CrawlerBase):
    def crawl(self, pub_date):
        pass # Comic no longer published
