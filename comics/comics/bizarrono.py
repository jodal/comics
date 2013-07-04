from comics.aggregator.crawler import CrawlerBase
from comics.core.comic_data import ComicDataBase


class ComicData(ComicDataBase):
    name = 'Bizarro (no)'
    language = 'no'
    url = 'http://underholdning.no.msn.com/tegneserier/bizarro/'
    start_date = '1985-01-01'
    active = False
    rights = 'Dan Piraro'


class Crawler(CrawlerBase):
    def crawl(self, pub_date):
        pass  # Comic no longer published
