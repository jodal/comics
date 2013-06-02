# encoding: utf-8

from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.core.comic_data import ComicDataBase

class ComicData(ComicDataBase):
    name = 'Dilbert (heltnormalt.no)'
    language = 'no'
    url = 'http://heltnormalt.no/dilbert'
    rights = 'Scott Adams'
	
class Crawler(CrawlerBase):
    history_capable_date='2013-02-01'
    time_zone = 'Europe/Oslo'

    def crawl(self, pub_date):
        url = 'http://heltnormalt.no/img/dilbert/%s.jpg' % (
            pub_date.strftime('%Y/%m/%d'))
        return CrawlerImage(url)
