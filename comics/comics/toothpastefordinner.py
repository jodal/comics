from comics.aggregator.crawler import CrawlerBase
from comics.core.comic_data import ComicDataBase


class ComicData(ComicDataBase):
    name = 'Toothpaste for Dinner'
    language = 'en'
    url = 'http://www.toothpastefordinner.com/'
    start_date = '2004-01-01'
    active = False
    rights = 'Drew'


class Crawler(CrawlerBase):
    def crawl(self, pub_date):
        pass  # Comic dislikes being read outside official page
