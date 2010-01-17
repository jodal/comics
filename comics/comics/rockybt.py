from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.meta.base import MetaBase

class Meta(MetaBase):
    name = 'Rocky (bt.no)'
    language = 'no'
    url = 'http://www.bt.no/tegneserier/rocky/'
    start_date = '1998-01-01'
    rights = 'Martin Kellerman'

class Crawler(CrawlerBase):
    history_capable_days = 162
    schedule = 'Mo,Tu,We,Th,Fr,Sa,Su'
    time_zone = 1

    def crawl(self, pub_date):
        url = 'http://images.bt.no/gfx/cartoons/rocky/%s.gif' % (
            pub_date.strftime('%d%m%y'),)
        return CrawlerImage(url)
