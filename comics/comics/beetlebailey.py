from comics.aggregator.crawler import KingFeaturesCrawlerBase
from comics.core.comic_data import ComicDataBase


class ComicData(ComicDataBase):
    name = 'Beetle Bailey'
    language = 'en'
    url = 'http://beetlebailey.com'
    start_date = '1950-01-01'
    rights = 'Mort Walker'


class Crawler(KingFeaturesCrawlerBase):
    history_capable_date = '1996-07-07'
    schedule = 'Mo,Tu,We,Th,Fr,Sa,Su'
    time_zone = 'US/Eastern'

    def crawl(self, pub_date):
        return self.crawl_helper('beetlebailey.com', pub_date)
