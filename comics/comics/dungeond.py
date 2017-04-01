from comics.aggregator.crawler import CrawlerBase
from comics.core.comic_data import ComicDataBase


class ComicData(ComicDataBase):
    name = 'Dungeons & Denizens'
    language = 'en'
    url = 'http://dungeond.com/'
    start_date = '2005-08-23'
    end_date = '2014-03-05'
    active = False
    rights = 'Graveyard Greg'


class Crawler(CrawlerBase):
    def crawl(self, pub_date):
        pass  # Comic no longer published
