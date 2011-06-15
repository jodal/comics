from comics.aggregator.crawler import GoComicsComCrawlerBase
from comics.meta.base import MetaBase

class Meta(MetaBase):
    name = 'Betty'
    language = 'en'
    url = 'http://www.gocomics.com/betty/'
    start_date = '1991-01-01'
    rights = 'Delainey & Gerry Rasmussen'

class Crawler(GoComicsComCrawlerBase):
    history_capable_date = '2008-10-13'
    schedule = 'Mo,Tu,We,Th,Fr,Sa,Su'
    time_zone = -5

    def crawl(self, pub_date):
        return self.crawl_helper('Betty', pub_date)
