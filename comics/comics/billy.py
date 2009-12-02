from comics.aggregator.crawler import CrawlerBase, CrawlerResult
from comics.meta.base import MetaBase

class Meta(MetaBase):
    name = 'Billy'
    language = 'no'
    url = 'http://www.billy.no/'
    start_date = '1950-01-01'
    history_capable_days = 6
    schedule = 'Mo,Tu,We,Th,Fr,Sa,Su'
    time_zone = 1
    rights = 'Mort Walker'

class Crawler(CrawlerBase):
    def crawl(self, pub_date):
        url = 'http://cserver.it-content.com/retriever.php?id=104&date=%(date)s' % {
            'date': pub_date.strftime('%Y%m%d'),
        }
        return CrawlerResult(url)
