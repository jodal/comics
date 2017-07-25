from comics.aggregator.crawler import KingFeaturesCrawlerBase
from comics.core.comic_data import ComicDataBase


class ComicData(ComicDataBase):
    name = 'Zits'
    language = 'en'
    url = 'http://zitscomics.com/'
    start_date = '1997-07-01'
    rights = 'Jerry Scott and Jim Borgman'


class Crawler(KingFeaturesCrawlerBase):
    history_capable_date = '2005-01-01'
    schedule = 'Mo,Tu,We,Th,Fr,Sa,Su'
    time_zone = 'US/Eastern'

    def crawl(self, pub_date):
        return self.crawl_helper('zitscomics.com', pub_date)
