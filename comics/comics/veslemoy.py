# encoding: utf-8

from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.meta.base import MetaBase

class Meta(MetaBase):
    name = 'Veslemøy'
    language = 'no'
    url = 'http://www.side2.no/tegneserie/veslemoy/'
    start_date = '2008-11-14'
    rights = 'Vantina Nina Andreassen'

class Crawler(CrawlerBase):
    history_capable_date = '2008-11-14'
    schedule = 'Mo,Tu,We,Th,Fr'
    time_zone = 1

    def crawl(self, pub_date):
        url = 'http://pub.tv2.no/nettavisen/tegneserie/pondus/veslemoy/%s.jpg' % (
            pub_date.strftime('%d%m%y'),)
        return CrawlerImage(url)
