# encoding: utf-8

from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.core.comic_data import ComicDataBase


class ComicData(ComicDataBase):
    name = 'Walk of Life'
    language = 'no'
    url = 'http://walkoflife.nettserier.no/'
    start_date = '2008-06-23'
    rights = 'Trond J. Stavås'


class Crawler(CrawlerBase):
    history_capable_date = '2008-06-23'
    schedule = 'Tu,Fr'
    time_zone = 'Europe/Oslo'

    def crawl(self, pub_date):
        epoch = self.date_to_epoch(pub_date)
        url = 'http://walkoflife.nettserier.no/_striper/walkoflife-%s.png' % (
            epoch,)
        return CrawlerImage(url)
