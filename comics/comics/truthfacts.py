from comics.aggregator.crawler import HeltNormaltCrawlerBase
from comics.core.comic_data import ComicDataBase


class ComicData(ComicDataBase):
    name = 'Truth Facts'
    language = 'no'
    url = 'http://heltnormalt.no/truthfacts'


class Crawler(HeltNormaltCrawlerBase):
    history_capable_date = '2013-02-12'
    schedule = 'Mo,Tu,We,Th,Fr'

    def crawl(self, pub_date):
        return self.crawl_helper('truth_facts', pub_date)
