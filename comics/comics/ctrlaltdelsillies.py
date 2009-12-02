from comics.aggregator.crawler import CrawlerBase, CrawlerResult
from comics.meta.base import MetaBase

class Meta(MetaBase):
    name = 'Ctrl+Alt+Del Sillies'
    language = 'en'
    url = 'http://www.ctrlaltdel-online.com/'
    start_date = '2008-06-27'
    history_capable_date = '2008-06-27'
    schedule = 'Mo,Tu,We,Th,Fr,Sa,Su'
    time_zone = -5
    rights = 'Tim Buckley'

class Crawler(CrawlerBase):
    def crawl(self, pub_date):
        url = 'http://www.ctrlaltdel-online.com/comics/Lite%(date)s.gif' % {
            'date': pub_date.strftime('%Y%m%d'),
        }
        return CrawlerResult(url)
