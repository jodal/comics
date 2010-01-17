# encoding: utf-8

from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.meta.base import MetaBase

class Meta(MetaBase):
    name = 'Pondus (bt.no)'
    language = 'no'
    url = 'http://www.bt.no/tegneserier/?type=pondus'
    start_date = '1995-01-01'
    rights = 'Frode Øverli'

class Crawler(CrawlerBase):
    history_capable_days = 14
    schedule = 'Mo,Tu,We,Th,Fr,Sa,Su'
    time_zone = 1

    def crawl(self, pub_date):
        url = 'http://images.bt.no/gfx/cartoons/pondus/%s.gif' % (
            pub_date.strftime('%d%m%y'),)
        return CrawlerImage(url)
