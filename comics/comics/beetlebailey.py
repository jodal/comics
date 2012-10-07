from comics.aggregator.crawler import ArcaMaxCrawlerBase
from comics.core.comic_data import ComicDataBase

class ComicData(ComicDataBase):
    name = 'Beetle Bailey'
    language = 'en'
    url = 'http://www.arcamax.com/thefunnies/beetlebailey/'
    start_date = '1950-01-01'
    rights = 'Mort Walker'

class Crawler(ArcaMaxCrawlerBase):
    history_capable_days = 0
    schedule = 'Mo,Tu,We,Th,Fr,Sa,Su'
    time_zone = 'US/Eastern'

    def crawl(self, pub_date):
        return self.crawl_helper('beetlebailey', pub_date)
