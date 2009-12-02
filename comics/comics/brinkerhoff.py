from comics.aggregator.crawler import CrawlerBase, CrawlerResult
from comics.meta.base import MetaBase

class Meta(MetaBase):
    name = 'Brinkerhoff'
    language = 'en'
    url = 'http://www.brinkcomic.com/'
    start_date = '2006-01-02'
    rights = 'Gabe Strine'

class Crawler(CrawlerBase):
    history_capable_date = '2006-01-02'
    schedule = 'Mo,Tu,We,Th,Fr'
    time_zone = -5

    def crawl(self, pub_date):
        url = 'http://www.brinkcomic.com/comics/%s.gif' % (
            pub_date.strftime('%Y%m%d'),)
        headers = {
            'Referer': 'http://www.brinkcomic.com/d/%s/' % (
                pub_date.strftime('%Y%m%d'),)
        }
        return CrawlerResult(url, headers=headers)
