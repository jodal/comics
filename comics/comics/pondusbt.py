# encoding: utf-8

from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.comics.pondus import Meta as PondusMeta

class Meta(PondusMeta):
    name = 'Pondus (bt.no)'
    url = 'http://www.bt.no/tegneserier/?type=pondus'

class Crawler(CrawlerBase):
    history_capable_days = 14
    schedule = 'Mo,Tu,We,Th,Fr,Sa'
    time_zone = 1

    def crawl(self, pub_date):
        url = 'http://images.bt.no/gfx/cartoons/pondus/%s.gif' % (
            pub_date.strftime('%d%m%y'),)
        return CrawlerImage(url)
