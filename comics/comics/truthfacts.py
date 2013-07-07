# encoding: utf-8

from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.core.comic_data import ComicDataBase


class ComicData(ComicDataBase):
    name = 'Truth Facts'
    language = 'no'
    url = 'http://heltnormalt.no/truthfacts'


class Crawler(CrawlerBase):
    history_capable_date = '2013-02-12'
    schedule = 'Mo,Tu,We,Th,Fr'
    time_zone = 'Europe/Oslo'

    def crawl(self, pub_date):
        url = 'http://heltnormalt.no/img/truth_facts/%s.jpg' % (
            pub_date.strftime('%Y/%m/%d'))
        return CrawlerImage(url)
