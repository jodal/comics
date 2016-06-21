# encoding: utf-8

from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.core.comic_data import ComicDataBase


class ComicData(ComicDataBase):
    name = 'Hägar the Horrible'
    language = 'en'
    url = 'http://www.hagardunor.net/'
    start_date = '1973-02-04'
    rights = 'Chris Browne'


class Crawler(CrawlerBase):
    history_capable_date = '2005-10-15'
    schedule = 'Mo,Tu,We,Th,Fr,Sa,Su'
    time_zone = 'Europe/Oslo'


    def crawl(self, pub_date):
        url = 'http://www.hagardunor.net/stripus%s/Hagar_The_Horrible_%s.gif' % (
            pub_date.strftime('%Y'),
            pub_date.strftime('%Y%m%d')
)
        return CrawlerImage(url)
