# encoding: utf-8
from comics.aggregator.crawler import ComicsKingdomCrawlerBase
from comics.core.comic_data import ComicDataBase


class ComicData(ComicDataBase):
    name = 'Hägar the Horrible'
    language = 'en'
    url = 'https://www.comicskingdom.com/hagar-the-horrible'
    rights = 'Chris Browne'


class Crawler(ComicsKingdomCrawlerBase):
    history_capable_days = 6
    schedule = 'Mo,Tu,We,Th,Fr,Sa,Su'
    time_zone = 'US/Eastern'

    def crawl(self, pub_date):
        return self.crawl_helper('hagar-the-horrible', pub_date)
