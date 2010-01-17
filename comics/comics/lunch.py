# encoding: utf-8

from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.meta.base import MetaBase

class Meta(MetaBase):
    name = 'Lunch'
    language = 'no'
    url = 'http://www.nettavisen.no/tegneserie/striper/'
    start_date = '2009-10-21'
    rights = 'Børge Lund'

class Crawler(CrawlerBase):
    history_capable_date = '2009-10-21'
    schedule = 'We'
    time_zone = 1

    def crawl(self, pub_date):
        url = 'http://pub.tv2.no/nettavisen/tegneserie/pondus/lunch/%s.gif' % (
            pub_date.strftime('%d%m%y'),)
        return CrawlerImage(url)
