from comics.aggregator.crawler import ComicsKingdomCrawlerBase
from comics.core.comic_data import ComicDataBase


class ComicData(ComicDataBase):
    name = 'Zits'
    language = 'en'
    url = 'http://zitscomics.com/'
    start_date = '1997-07-01'
    rights = 'Jerry Scott and Jim Borgman'


class Crawler(ComicsKingdomCrawlerBase):
    history_capable_days = 6
    schedule = 'Mo,Tu,We,Th,Fr,Sa,Su'
    time_zone = 'US/Eastern'

    def crawl(self, pub_date):
        return self.crawl_helper('zits', pub_date)
