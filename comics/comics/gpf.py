from comics.aggregator.crawler import CrawlerBase, CrawlerResult
from comics.meta.base import MetaBase

class Meta(MetaBase):
    name = 'General Protection Fault'
    language = 'en'
    url = 'http://www.gpf-comics.com/'
    start_date = '1998-11-02'
    history_capable_date = '1998-11-02'
    schedule = 'Mo,We,Fr'
    time_zone = -5
    rights = 'Jeffrey T. Darlington'

class Crawler(CrawlerBase):
    def crawl(self, pub_date):
        page_url = 'http://www.gpf-comics.com/archive.php?d=%(date)s' % {
            'date': pub_date.strftime('%Y%m%d'),
        }
        page = self.parse_page(page_url)
        url = page.src('img[alt^="[Comic for"]')
        return CrawlerResult(url)
