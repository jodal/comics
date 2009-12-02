from comics.aggregator.crawler import ComicsComCrawlerBase
from comics.meta.base import MetaBase

class Meta(MetaBase):
    name = 'Betty'
    language = 'en'
    url = 'http://comics.com/betty/'
    start_date = '1991-01-01'
    history_capable_date = '2008-10-13'
    schedule = 'Mo,Tu,We,Th,Fr,Sa,Su'
    time_zone = -5
    rights = 'Delainey & Gerry Rasmussen'

class Crawler(ComicsComCrawlerBase):
    def crawl(self, pub_date):
        return self.crawl_helper('Betty', pub_date)
