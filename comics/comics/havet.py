# encoding: utf-8

from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.core.comic_data import ComicDataBase

class ComicData(ComicDataBase):
    name = 'Havet'
    language = 'no'
    url = 'http://havet.nettserier.no/'
    start_date = '2007-09-27'
    rights = 'Øystein Ottesen'

class Crawler(CrawlerBase):
    history_capable_days = 90
    schedule = 'We'
    time_zone = 1

    def crawl(self, pub_date):
        url = 'http://havet.nettserier.no/_striper/havet-%s.jpg' % (
            self.date_to_epoch(pub_date),)
        return CrawlerImage(url)
