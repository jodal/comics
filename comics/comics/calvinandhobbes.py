from comics.aggregator.crawler import CrawlerBase, CrawlerResult
from comics.meta.base import MetaBase

class Meta(MetaBase):
    name = 'Calvin and Hobbes'
    language = 'en'
    url = 'http://www.calvinandhobbes.com/'
    start_date = '1985-11-18'
    end_date = '1995-12-31'
    history_capable_days = 31
    schedule = 'Mo,Tu,We,Th,Fr,Sa,Su'
    rights = 'Bill Watterson'

class Crawler(CrawlerBase):
    def crawl(self, pub_date):
        url = 'http://images.ucomics.com/comics/ch/%(year)s/ch%(date)s.gif' % {
            'year': pub_date.strftime('%Y'),
            'date': pub_date.strftime('%y%m%d'),
        }
        return CrawlerResult(url)
