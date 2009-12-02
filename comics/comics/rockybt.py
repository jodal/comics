from comics.aggregator.crawler import CrawlerBase, CrawlerResult
from comics.meta.base import MetaBase

class Meta(MetaBase):
    name = 'Rocky (bt.no)'
    language = 'no'
    url = 'http://www.bt.no/tegneserier/rocky/'
    start_date = '1998-01-01'
    history_capable_days = 162
    schedule = 'Mo,Tu,We,Th,Fr,Sa,Su'
    time_zone = 1
    rights = 'Martin Kellerman'

class Crawler(CrawlerBase):
    def crawl(self, pub_date):
        url = 'http://images.bt.no/gfx/cartoons/rocky/%(date)s.gif' % {
            'date': pub_date.strftime('%d%m%y'),
        }
        return CrawlerResult(url)
