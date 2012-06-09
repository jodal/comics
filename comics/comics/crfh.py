from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.meta.base import MetaBase

class Meta(MetaBase):
    name = 'Colleges Roomies from Hell'
    language = 'en'
    url = 'http://www.crfh.net/'
    start_date = '1999-01-01'
    rights = 'Maritza Campos'

class Crawler(CrawlerBase):
    history_capable_date = '1999-01-01'
    time_zone = -5

    def crawl(self, pub_date):
        page_url = 'http://www.crfh.net/d2/%s.html' % (
            pub_date.strftime('%Y%m%d'),)
        page = self.parse_page(page_url)
        url = page.src('img[src*="crfh%s"]' % pub_date.strftime('%Y%m%d'))
        url = url.replace('\n', '')
        return CrawlerImage(url)
