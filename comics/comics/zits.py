from comics.aggregator.crawler import ArcaMaxCrawlerBase
from comics.core.comic_data import ComicDataBase

class ComicData(ComicDataBase):
    name = 'Zits'
    language = 'en'
    url = 'http://www.arcamax.com/zits'
    start_date = '1997-07-01'
    rights = 'Jerry Scott and Jim Borgman'

class Crawler(ArcaMaxCrawlerBase):
    history_capable_days = 0
    schedule = 'Mo,Tu,We,Th,Fr,Sa,Su'
    time_zone = -5

    def crawl(self, pub_date):
        return self.crawl_helper('zits', pub_date)
