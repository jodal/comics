# encoding: utf-8

from comics.aggregator.crawler import NettserierCrawlerBase
from comics.core.comic_data import ComicDataBase


class ComicData(ComicDataBase):
    name = 'Uten Sokker'
    language = 'no'
    url = 'http://utensokker.nettserier.no/'
    start_date = '2009-07-14'
    rights = 'Bjørnar Grandalen'


class Crawler(NettserierCrawlerBase):
    history_capable_date = '2009-07-14'
    time_zone = 'Europe/Oslo'

    def crawl(self, pub_date):
        return self.crawl_helper('utensokker',pub_date)