from comics.aggregator.crawler import ComicsComCrawlerBase
from comics.meta.base import MetaBase

class Meta(MetaBase):
    name = 'Pearls Before Swine'
    language = 'en'
    url = 'http://comics.com/pearls_before_swine/'
    start_date = '2001-12-30'
    rights = 'Stephan Pastis'

class Crawler(ComicsComCrawlerBase):
    history_capable_date = '2002-01-06'
    schedule = 'Mo,Tu,We,Th,Fr,Sa,Su'
    time_zone = -5

    def crawl(self, pub_date):
        return self.crawl_helper('Pearls Before Swine', pub_date)
