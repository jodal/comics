from comics.aggregator.crawler import CrawlerBase, CrawlerResult
from comics.meta.base import MetaBase

class Meta(MetaBase):
    name = 'Diesel Sweeties (print)'
    language = 'en'
    url = 'http://www.dieselsweeties.com/'
    start_date = '2007-01-01'
    history_capable_date = '2007-01-01'
    schedule = 'Mo,Tu,We,Th,Fr,Sa,Su'
    time_zone = -5
    rights = 'Richard Stevens'

class Crawler(CrawlerBase):
    def crawl(self, pub_date):
        url = 'http://www.dieselsweeties.com/print/strips/ds%(date)s.png' % {
            'date': pub_date.strftime('%Y%m%d'),
        }
        return CrawlerResult(url)
