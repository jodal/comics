from comics.aggregator.crawler import CrawlerBase
from comics.core.comic_data import ComicDataBase

class ComicData(ComicDataBase):
    name = 'Morten M'
    language = 'no'
    url = 'http://www.vg.no/spesial/mortenm/'
    start_date = '1978-01-01'
    end_date = '2011-12-31'
    active = False
    rights = 'Morten M. Kristiansen'

class Crawler(CrawlerBase):
    def crawl(self, pub_date):
        pass # Comic no longer published
