from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.core.comic_data import ComicDataBase


class ComicData(ComicDataBase):
    name = 'Dilbert (vg.no)'
    language = 'no'
    url = 'http://heltnormalt.no/dilbert'
    start_date = '1989-04-16'
    rights = 'Scott Adams'


class Crawler(CrawlerBase):
    history_capable_date = '2013-02-01'
    schedule = 'Mo,Tu,We,Th,Fr,Sa,Su'
    time_zone = 'Europe/Oslo'

    def crawl(self, pub_date):
        url = 'http://heltnormalt.no/img/dilbert/%s.jpg' % (
            pub_date.strftime('%Y/%m/%d'))
        return CrawlerImage(url)
