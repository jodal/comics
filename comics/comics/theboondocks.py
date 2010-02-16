from comics.aggregator.crawler import GoComicsComCrawlerBase
from comics.meta.base import MetaBase

class Meta(MetaBase):
    name = 'The Boondocks'
    language = 'en'
    url = 'http://www.gocomics.com/theboondocks'
    start_date = '1999-04-19'
    rights = 'Aaron McGruder'

class Crawler(GoComicsComCrawlerBase):
    history_capable_date = '1999-04-19'
    schedule = 'Mo,Tu,We,Th,Fr,Sa,Su'
    time_zone = -5

    def crawl(self, pub_date):
        return self.crawl_helper('The Boondocks', pub_date, 'boondocks')
