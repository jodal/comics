# encoding: utf-8

from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.core.comic_data import ComicDataBase

class ComicData(ComicDataBase):
    name = 'Lunch (db.no)'
    language = 'no'
    url = 'http://www.dagbladet.no/tegneserie/lunch/'
    start_date = '2009-10-21'
    rights = 'Børge Lund'

class Crawler(CrawlerBase):
    history_capable_days = 14
    schedule = 'Mo,Tu,We,Th,Fr,Sa'
    time_zone = 'Europe/Oslo'

    def crawl(self, pub_date):
        epoch = self.date_to_epoch(pub_date, 'Europe/Oslo')
        url = 'http://www.dagbladet.no/tegneserie/luncharkiv/serve.php?%s' % (
            epoch,)
        return CrawlerImage(url)
