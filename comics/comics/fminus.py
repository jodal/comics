from comics.aggregator.crawler import GoComicsComCrawlerBase
from comics.meta.base import MetaBase

class Meta(MetaBase):
    name = 'F Minus'
    language = 'en'
    url = 'http://comics.com/f_minus/'
    start_date = '1999-09-01'
    rights = 'Tony Carrillo'

class Crawler(GoComicsComCrawlerBase):
    history_capable_date = '2001-02-02'
    schedule = 'Mo,Tu,We,Th,Fr,Sa,Su'
    time_zone = -5

    def crawl(self, pub_date):
        return self.crawl_helper('F Minus', pub_date)
