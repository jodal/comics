import datetime

from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.core.comic_data import ComicDataBase


class ComicData(ComicDataBase):
    name = 'Wulffmorgenthaler'
    language = 'en'
    url = 'http://www.wumo.com/'
    start_date = '2001-01-01'
    rights = 'Mikael Wulff & Anders Morgenthaler'


class Crawler(CrawlerBase):
    history_capable_days = 20
    schedule = 'Mo,Tu,We,Th,Fr,Sa,Su'
    time_zone = 'Europe/Copenhagen'

    def crawl(self, pub_date):
        feed = self.parse_feed('http://feeds.feedburner.com/wulffmorgenthaler')
        for entry in feed.for_date(pub_date):
            url = entry.summary.src('img[src^="http://wumo.com/"]')
            return CrawlerImage(url)
