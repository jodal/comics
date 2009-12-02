from comics.aggregator.crawler import CrawlerBase, CrawlerResult
from comics.meta.base import MetaBase

class Meta(MetaBase):
    name = 'User Friendly'
    language = 'en'
    url = 'http://www.userfriendly.org/'
    start_date = '1997-11-17'
    history_capable_date = '1997-11-17'
    schedule = 'Mo,Tu,We,Th,Fr,Sa,Su'
    rights = 'J.D. "Illiad" Frazer'

class Crawler(CrawlerBase):
    def crawl(self, pub_date):
        page_url = 'http://ars.userfriendly.org/cartoons/?id=%(date)s' % {
            'date': pub_date.strftime('%Y%m%d'),
        }
        page = self.parse_page(page_url)
        url = page.src('img[alt^="Strip for"]')
        return CrawlerResult(url)
