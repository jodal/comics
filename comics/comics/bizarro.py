from comics.aggregator.crawler import KingFeaturesCrawlerBase
from comics.core.comic_data import ComicDataBase


class ComicData(ComicDataBase):
    name = 'Bizarro'
    language = 'en'
    url = 'http://bizarrocomics.com/'
    start_date = '1985-01-01'
    rights = 'Dan Piraro'


class Crawler(KingFeaturesCrawlerBase):
    history_capable_date = '1996-02-04'
    schedule = 'Mo,Tu,We,Th,Fr,Sa,Su'
    time_zone = 'US/Eastern'

    def crawl(self, pub_date):
        return self.crawl_helper('bizarro.com', pub_date)
