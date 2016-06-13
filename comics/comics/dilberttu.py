# encoding: utf-8

from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.core.comic_data import ComicDataBase


class ComicData(ComicDataBase):
    name = 'Dilbert (tu.no)'
    language = 'no'
    url = 'http://www.tu.no/dilbert/'
    start_date = '2009-10-21'
    rights = 'Scott Adams'


class Crawler(CrawlerBase):
    history_capable_date = '2012-06-15'
    schedule = 'Mo,Tu,We,Th,Fr'
    time_zone = 'Europe/Oslo'

    # Without referer, the server returns a placeholder image
#    headers = {'Referer': 'http://www.tu.no/tegneserier/lunch/'}

    def crawl(self, pub_date):
        url = 'http://www.tu.no/?module=TekComics&service=image&id=dilbert&key=%s' % (
            pub_date.strftime('%Y-%m-%d'))
        return CrawlerImage(url)
