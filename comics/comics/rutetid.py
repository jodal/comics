# encoding: utf-8

from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.core.comic_data import ComicDataBase


class ComicData(ComicDataBase):
    name = 'Rutetid'
    language = 'no'
    url = 'http://www.dagbladet.no/tegneserie/rutetid/'
    rights = 'Frode Øverli'


class Crawler(CrawlerBase):
    history_capable_days = 10
    schedule = 'Mo,Tu,We,Th,Fr'
    time_zone = 'Europe/Oslo'

    def crawl(self, pub_date):
        epoch = self.date_to_epoch(pub_date)
        url = 'http://www.dagbladet.no/tegneserie/pondusarkiv/serveconfig.php?strip=rutetid&date=%s' % (
            epoch,)
        return CrawlerImage(url)
