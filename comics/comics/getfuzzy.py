from comics.aggregator.crawler import ComicsComCrawlerBase
from comics.meta.base import MetaBase

class Meta(MetaBase):
    name = 'Get Fuzzy'
    language = 'en'
    url = 'http://comics.com/get_fuzzy/'
    start_date = '1999-09-01'
    history_capable_date = '2009-05-26'
    schedule = 'Mo,Tu,We,Th,Fr,Sa,Su'
    time_zone = -5
    rights = 'Darby Conley'

class Crawler(ComicsComCrawlerBase):
    def crawl(self, pub_date):
        return self.crawl_helper('Get Fuzzy', pub_date)
