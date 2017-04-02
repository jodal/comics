from comics.aggregator.crawler import DagbladetCrawlerBase
from comics.core.comic_data import ComicDataBase


class ComicData(ComicDataBase):
    name = 'Zelda'
    language = 'no'
    url = 'http://www.dagbladet.no/tegneserie/zelda-lille-berlin/'
    start_date = '2012-06-07'
    rights = 'Lina Neidestam'


class Crawler(DagbladetCrawlerBase):
    history_capable_date = '2012-06-07'
    schedule = 'Mo,Tu,We,Th,Fr,Sa'
    time_zone = 'Europe/Oslo'

    def crawl(self, pub_date):
        return self.crawl_helper('zelda-lille-berlin',pub_date)
