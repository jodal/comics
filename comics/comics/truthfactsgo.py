from comics.aggregator.crawler import GoComicsComCrawlerBase
from comics.core.comic_data import ComicDataBase


class ComicData(ComicDataBase):
    name = 'Truth Facts (gocomics.com)'
    language = 'en'
    url = 'http://www.gocomics.com/truth-facts'
    rights = 'Wulff & Morgenthaler'


class Crawler(GoComicsComCrawlerBase):
    history_capable_date = '2014-06-16'
    schedule = 'Mo,Tu,We,Th,Fr,Sa,Su'
    time_zone = 'Europe/Oslo'

    def crawl(self, pub_date):
        return self.crawl_helper('truth-facts', pub_date)
