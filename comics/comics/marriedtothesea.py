from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.core.comic_data import ComicDataBase


class ComicData(ComicDataBase):
    name = 'Married To The Sea'
    language = 'en'
    url = 'http://www.marriedtothesea.com/'
    start_date = '2006-02-13'
    active = False
    rights = 'Drew'


class Crawler(CrawlerBase):
    def crawl(self, pub_date):
        pass  # Comic dislikes being read outside official page
