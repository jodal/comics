from comics.aggregator.crawler import NettserierCrawlerBase
from comics.core.comic_data import ComicDataBase


class ComicData(ComicDataBase):
    name = 'Ikke Saro'
    language = 'no'
    url = 'http://ikkesaro.nettserier.no/'
    rights = 'Ladder'


class Crawler(NettserierCrawlerBase):
    history_capable_date = '2016-06-16'
    time_zone = 'Europe/Oslo'

    def crawl(self, pub_date):
        return self.crawl_helper('ikkesaro', pub_date)
