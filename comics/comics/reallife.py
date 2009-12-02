from comics.aggregator.crawler import CrawlerBase, CrawlerResult
from comics.meta.base import MetaBase

class Meta(MetaBase):
    name = 'Real Life'
    language = 'en'
    url = 'http://www.reallifecomics.com/'
    start_date = '1999-11-15'
    history_capable_date = '1999-11-15'
    schedule = 'Mo,Tu,We,Th,Fr'
    rights = 'Greg Dean'

class Crawler(CrawlerBase):
    def crawl(self, pub_date):
        page_url = 'http://www.reallifecomics.com/archive/%(date)s.html' % {
            'date': pub_date.strftime('%y%m%d'),
        }
        page = self.parse_page(page_url)
        url = page.src('img[alt^="strip for"]')
        return CrawlerResult(url)
