# encoding: utf-8

from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.meta.base import MetaBase

class Meta(MetaBase):
    name = 'Pondus (db.no)'
    language = 'no'
    url = 'http://www.dagbladet.no/tegneserie/pondus/'
    start_date = '1995-01-01'
    rights = 'Frode Øverli'

class Crawler(CrawlerBase):
    history_capable_days = 30
    schedule = 'Mo,Tu,We,Th,Fr,Sa'
    time_zone = 1

    def crawl(self, pub_date):
        page_url = 'http://www.dagbladet.no/tegneserie/pondus/?%s' % (
            self.date_to_epoch(pub_date),)
        page = self.parse_page(page_url)
        url = page.src('img#pondus-stripe')
        return CrawlerImage(url)
