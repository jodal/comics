from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.core.comic_data import ComicDataBase


class ComicData(ComicDataBase):
    name = 'Wulffmorgenthaler (vg.no)'
    language = 'no'
    url = 'http://heltnormalt.no/wumo'
    rights = 'Mikael Wulff & Anders Morgenthaler'


class Crawler(CrawlerBase):
    history_capable_date = '2013-01-26'
    time_zone = 'Europe/Oslo'

    def crawl(self, pub_date):
        url = 'http://heltnormalt.no/img/wumo/%s.jpg' % (
            pub_date.strftime('%Y/%m/%d'))
        return CrawlerImage(url)
