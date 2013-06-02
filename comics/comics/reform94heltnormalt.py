# encoding: utf-8

from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.core.comic_data import ComicDataBase

class ComicData(ComicDataBase):
    name = 'Reform 94 (heltnormalt.no)'
    language = 'no'
    url = 'http://heltnormalt.no/reform94'
    start_date = '2012-01-01'
    rights = 'Jorunn Hanto-Haugse'
	
class Crawler(CrawlerBase):
    history_capable_date='2013-03-08'
    time_zone = 'Europe/Oslo'

    def crawl(self, pub_date):
        url = 'http://heltnormalt.no/img/reform94/%s.jpg' % (
            pub_date.strftime('%Y/%m/%d'))
        return CrawlerImage(url)
