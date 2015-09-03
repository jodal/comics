from comics.aggregator.crawler import KingFeaturesCrawlerBase
from comics.core.comic_data import ComicDataBase


class ComicData(ComicDataBase):
    name = 'Baby Blues'
    language = 'en'
    url = 'http://www.babyblues.com'
    start_date = '1990-01-01'
    rights = 'Rick Kirkman and Jerry Scott'


class Crawler(KingFeaturesCrawlerBase):
    history_capable_date = '1995-01-08'
    schedule = 'Mo,Tu,We,Th,Fr,Sa,Su'
    time_zone = 'US/Eastern'

    def crawl(self, pub_date):
        return self.crawl_helper('babyblues.com', pub_date)
