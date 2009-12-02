from comics.aggregator.crawler import CrawlerBase, CrawlerResult
from comics.meta.base import MetaBase

class Meta(MetaBase):
    name = 'Sinfest'
    language = 'en'
    url = 'http://www.sinfest.net/'
    start_date = '2001-01-17'
    history_capable_date = '2001-01-17'
    schedule = 'Mo,Tu,We,Th,Fr,Sa,Su'
    rights = 'Tatsuya Ishida'

class Crawler(CrawlerBase):
    def crawl(self, pub_date):
        url = 'http://www.sinfest.net/comikaze/comics/%(date)s.gif' % {
            'date': pub_date.strftime('%Y-%m-%d'),
        }
        return CrawlerResult(url)
