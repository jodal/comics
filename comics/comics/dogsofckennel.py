from comics.aggregator.crawler import CreatorsCrawlerBase
from comics.core.comic_data import ComicDataBase


class ComicData(ComicDataBase):
    name = 'Dogs of C-Kennel'
    language = 'en'
    url = 'https://www.creators.com/read/dogs-of-c-kennel'
    rights = 'Mason Mastroianni, Mick Mastroianni, Johnny Hart'


class Crawler(CreatorsCrawlerBase):
    history_capable_date = '2007-02-12'
    schedule = 'Mo,Tu,We,Th,Fr,Sa,Su'
    time_zone = 'US/Pacific'

    def crawl(self, pub_date):
        return self.crawl_helper('179', pub_date)
