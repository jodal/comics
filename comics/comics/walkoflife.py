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
    history_capable_days = 90
    schedule = 'Mo,We,Fr'
    time_zone = 1

    def crawl(self, pub_date):
        url = 'http://walkoflife.nettserier.no/_striper/walkoflife-%s.png' % (
            self.date_to_epoch(pub_date),)
        return CrawlerImage(url)
