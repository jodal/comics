from comics.aggregator.crawler import CrawlerBase, CrawlerResult
from comics.meta.base import MetaBase

class Meta(MetaBase):
    name = 'Gun Show'
    language = 'en'
    url = 'http://www.gunshowcomic.com/'
    start_date = '2008-09-04'
    history_capable_date = '2008-09-04'
    schedule = 'Mo,Tu,We,Th,Fr'
    rights = '"Lord KC Green"'

class Crawler(CrawlerBase):
    def crawl(self, pub_date):
        page_url = 'http://www.gunshowcomic.com/d/%(date)s.html' % {
            'date': pub_date.strftime('%Y%m%d'),
        }
        page = self.parse_page(page_url)
        url = page.src('img[src^="http://www.gunshowcomic.com/comics/"]')
        return CrawlerResult(url)
