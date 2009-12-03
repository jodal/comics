from comics.aggregator.crawler import CrawlerBase, CrawlerResult
from comics.meta.base import MetaBase

class Meta(MetaBase):
    name = 'Sinfest'
    language = 'en'
    url = 'http://www.sinfest.net/'
    start_date = '2001-01-17'
    rights = 'Tatsuya Ishida'

class Crawler(CrawlerBase):
    history_capable_date = '2001-01-17'
    schedule = 'Mo,Tu,We,Th,Fr,Sa,Su'

    def crawl(self, pub_date):
        url = 'http://www.sinfest.net/comikaze/comics/%s.gif' % (
            pub_date.strftime('%Y-%m-%d'),)
        return CrawlerResult(url)
