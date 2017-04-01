from comics.aggregator.crawler import CrawlerBase
from comics.core.comic_data import ComicDataBase


class ComicData(ComicDataBase):
    name = 'Beyond the Tree'
    language = 'en'
    url = 'http://beyondthetree.wordpress.com/'
    start_date = '2008-03-20'
    end_date = '2012-03-18'
    active = False
    rights = 'Nhani'


class Crawler(CrawlerBase):
    def crawl(self, pub_date):
        pass  # Comic no longer published
