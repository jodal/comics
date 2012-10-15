from comics.aggregator.crawler import ArcaMaxCrawlerBase
from comics.core.comic_data import ComicDataBase

class ComicData(ComicDataBase):
    name = 'Dustin'
    language = 'en'
    url = 'http://www.arcamax.com/thefunnies/dustin/'
    start_date = '2010-01-04'
    rights = 'Steve Kelley & Jeff Parker'

class Crawler(ArcaMaxCrawlerBase):
    history_capable_days = 0
    schedule = 'Mo,Tu,We,Th,Fr,Sa,Su'
    time_zone = 'US/Eastern'

    def crawl(self, pub_date):
        return self.crawl_helper('dustin', pub_date)
