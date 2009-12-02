from comics.aggregator.crawler import CrawlerBase, CrawlerResult
from comics.meta.base import MetaBase

class Meta(MetaBase):
    name = "Sherman's Lagoon"
    language = 'en'
    url = 'http://www.slagoon.com/'
    start_date = '1991-05-13'
    history_capable_days = 32
    schedule = 'Mo,Tu,We,Th,Fr,Sa,Su'
    time_zone = -5
    rights = 'Jim Toomey'

class Crawler(CrawlerBase):
    def crawl(self, pub_date):
        url = 'http://www.slagoon.com/dailies/SL%(date)s.gif' % {
            'date': pub_date.strftime('%y%m%d'),
        }
        return CrawlerResult(url)
