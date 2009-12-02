from comics.aggregator.crawler import CrawlerBase, CrawlerResult
from comics.meta.base import MetaBase

class Meta(MetaBase):
    name = 'Brinkerhoff'
    language = 'en'
    url = 'http://www.brinkcomic.com/'
    start_date = '2006-01-02'
    history_capable_date = '2006-01-02'
    schedule = 'Mo,Tu,We,Th,Fr'
    time_zone = -5
    rights = 'Gabe Strine'

class Crawler(CrawlerBase):
    def crawl(self, pub_date):
        url = 'http://www.brinkcomic.com/comics/%(date)s.gif' % {
            'date': pub_date.strftime('%Y%m%d'),
        }
        headers = {
            'Referer': 'http://www.brinkcomic.com/d/%(date)s/' % {
                'date': pub_date.strftime('%Y%m%d'),
            }
        }
        return CrawlerResult(url, headers=headers)
