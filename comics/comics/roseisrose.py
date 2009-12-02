from comics.aggregator.crawler import ComicsComCrawlerBase
from comics.meta.base import MetaBase

class Meta(MetaBase):
    name = 'Rose Is Rose'
    language = 'en'
    url = 'http://comics.com/rose_is_rose/'
    start_date = '1984-10-02'
    rights = 'Pat Brady'

class Crawler(ComicsComCrawlerBase):
    history_capable_date = '1995-10-09'
    schedule = 'Mo,Tu,We,Th,Fr,Sa,Su'
    time_zone = -5

    def crawl(self, pub_date):
        return self.crawl_helper('Rose Is Rose', pub_date)
