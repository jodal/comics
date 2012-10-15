# encoding: utf-8

from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.core.comic_data import ComicDataBase

class ComicData(ComicDataBase):
    name = 'Pondus (db.no)'
    language = 'no'
    url = 'http://www.dagbladet.no/tegneserie/pondus/'
    start_date = '1995-01-01'
    rights = 'Frode Øverli'

class Crawler(CrawlerBase):
    history_capable_days = 30
    schedule = 'Mo,Tu,We,Th,Fr,Sa'
    time_zone = 'Europe/Oslo'

    def crawl(self, pub_date):
        epoch = self.date_to_epoch(pub_date)
        page_url = 'http://www.dagbladet.no/tegneserie/pondus/?%s' % epoch
        page = self.parse_page(page_url)
        url = page.src('img#pondus-stripe')
        return CrawlerImage(url)
