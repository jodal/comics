from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.core.comic_data import ComicDataBase

class ComicData(ComicDataBase):
    name = 'Dilbert (vg.no)'
    language = 'no'
    url = 'http://www.vg.no/dilbert/'
    start_date = '1989-04-16'
    rights = 'Scott Adams'

class Crawler(CrawlerBase):
    history_capable_days = 0
    schedule = 'Mo,Tu,We,Th,Fr,Sa,Su'
    time_zone = 1

    def crawl(self, pub_date):
        url = 'http://static.vg.no/dilbert/dilbert.gif'
        return CrawlerImage(url)
