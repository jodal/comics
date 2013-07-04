# encoding: utf-8

from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.core.comic_data import ComicDataBase


class ComicData(ComicDataBase):
    name = 'Fagprat (db.no)'
    language = 'no'
    url = 'http://www.dagbladet.no/tegneserie/fagprat'
    rights = 'Flu Hartberg'


class Crawler(CrawlerBase):
    history_capable_date = '2010-11-15'
    schedule = 'Tu,Th,Sa'
    time_zone = 'Europe/Oslo'

    def crawl(self, pub_date):
        epoch = self.date_to_epoch(pub_date)
        url = (
            'http://www.dagbladet.no/tegneserie/' +
            'fagpratarkiv/serve.php?%d' % epoch)
        return CrawlerImage(url)
