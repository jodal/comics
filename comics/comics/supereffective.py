import datetime as dt

from comics.aggregator.crawler import CrawlerBase, CrawlerResult
from comics.meta.base import MetaBase

class Meta(MetaBase):
    name = 'Super Effective'
    language = 'en'
    url = 'http://www.vgcats.com/super/'
    start_date = '2008-04-23'
    history_capable_date = '2008-04-23'
    time_zone = -5
    rights = 'Scott Ramsoomair'

class Crawler(CrawlerBase):
    def crawl(self, pub_date):
        url = 'http://www.vgcats.com/super/images/%(date)s.gif' % {
            'date': pub_date.strftime('%y%m%d'),
        }
        return CrawlerResult(url)
