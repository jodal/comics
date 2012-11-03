# encoding: utf-8

from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.core.comic_data import ComicDataBase

class ComicData(ComicDataBase):
    name = 'Lunch (tu.no)'
    language = 'no'
    url = 'http://www.tu.no/lunch/'
    start_date = '2009-10-21'
    rights = 'Børge Lund'

class Crawler(CrawlerBase):
    schedule = 'Mo,Tu,We,Th,Fr'
    time_zone = 'Europe/Oslo'

    def crawl(self, pub_date):
        url = 'http://www1.tu.no/lunch/img/%s.png' % (
            pub_date.strftime('%y%m%d'))
        return CrawlerImage(url)