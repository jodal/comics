from comics.aggregator.crawler import GoComicsComCrawlerBase
from comics.meta.base import MetaBase

class Meta(MetaBase):
    name = 'Tank McNamara'
    language = 'en'
    url = 'http://www.gocomics.com/tankmcnamara'
    start_date = '1998-01-01'
    rights = 'Wiley Miller'

class Crawler(GoComicsComCrawlerBase):
    history_capable_date = '1998-01-01'
    schedule = 'Mo,Tu,We,Th,Fr,Sa,Su'
    time_zone = -5

    def crawl(self, pub_date):
        return self.crawl_helper('Tank McNamara', pub_date)
