from comics.aggregator.crawler import ComicsKingdomCrawlerBase
from comics.core.comic_data import ComicDataBase


class ComicData(ComicDataBase):
    name = 'Baby Blues'
    language = 'en'
    url = 'https://www.comicskingdom.com/baby-blues'
    start_date = '1990-01-01'
    rights = 'Rick Kirkman and Jerry Scott'


class Crawler(ComicsKingdomCrawlerBase):
    history_capable_days = 6
    schedule = 'Mo,Tu,We,Th,Fr,Sa,Su'
    time_zone = 'US/Eastern'

    def crawl(self, pub_date):
        return self.crawl_helper('baby-blues', pub_date)
