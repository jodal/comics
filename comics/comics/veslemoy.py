# encoding: utf-8

from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.core.comic_data import ComicDataBase

class ComicData(ComicDataBase):
    name = 'Veslemøy'
    language = 'no'
    url = 'http://www.side2.no/tegneserie/veslemoy/'
    start_date = '2008-11-14'
    end_date='2012-12-31'
    active = False
    rights = 'Vantina Nina Andreassen'

class Crawler(CrawlerBase):
    history_capable_date = '2008-11-14'
    schedule = 'Mo,We,Fr'
    time_zone = 'Europe/Oslo'

    def crawl(self, pub_date):
        url = ('http://pub.tv2.no/nettavisen/tegneserie/' +
            'pondus/veslemoy/%s.jpg' % pub_date.strftime('%d%m%y'))
        return CrawlerImage(url)
