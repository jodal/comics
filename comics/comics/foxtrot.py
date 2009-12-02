from comics.aggregator.crawler import CrawlerBase, CrawlerResult
from comics.meta.base import MetaBase

class Meta(MetaBase):
    name = 'FoxTrot'
    language = 'en'
    url = 'http://www.foxtrot.com/'
    start_date = '1988-04-10'
    history_capable_date = '2006-12-27'
    schedule = 'Su'
    time_zone = -5
    rights = 'Bill Amend'

class Crawler(CrawlerBase):
    def crawl(self, pub_date):
        url = 'http://images.ucomics.com/comics/ft/%(year)s/ft%(date)s.gif' % {
            'year': pub_date.strftime('%Y'),
            'date': pub_date.strftime('%y%m%d'),
        }
        return CrawlerResult(url)
