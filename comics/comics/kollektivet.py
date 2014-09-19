# encoding: utf-8

from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.core.comic_data import ComicDataBase


class ComicData(ComicDataBase):
    name = 'Kollektivet'
    language = 'no'
    url = 'http://heltnormalt.no/kollektivet'
    rights = 'Torbjørn Lien'


class Crawler(CrawlerBase):
    history_capable_date = '2013-05-01'
    schedule = 'Mo,Tu,We,Th,Fr,Sa'
    time_zone = 'Europe/Oslo'

    def crawl(self, pub_date):
        url = 'http://heltnormalt.no/img/kollektivet/%s.jpg' % (
            pub_date.strftime('%Y/%m/%d'))
        return CrawlerImage(url)
