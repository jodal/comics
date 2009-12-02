from comics.aggregator.crawler import ComicsComCrawlerBase
from comics.meta.base import MetaBase

class Meta(MetaBase):
    name = 'Peanuts'
    language = 'en'
    url = 'http://comics.com/peanuts/'
    start_date = '1950-10-02'
    end_date = '2000-02-13'
    rights = 'Charles M. Schulz'

class Crawler(ComicsComCrawlerBase):
    history_capable_date = '1950-10-02'
    schedule = 'Mo,Tu,We,Th,Fr,Sa,Su'

    def crawl(self, pub_date):
        return self.crawl_helper('Peanuts', pub_date)
