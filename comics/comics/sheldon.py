from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.meta.base import MetaBase

class Meta(MetaBase):
    name = 'Sheldon'
    language = 'en'
    url = 'http://www.sheldoncomics.com/'
    start_date = '2001-11-30'
    rights = 'Dave Kellett'

class Crawler(CrawlerBase):
    history_capable_date = Meta.start_date
    schedule = 'Mo,Tu,We,Th,Fr'
    time_zone = -5

    def crawl(self, pub_date):
        page_url = 'http://www.sheldoncomics.com/archive/%s.html' % (
            pub_date.strftime('%y%m%d'),)
        page = self.parse_page(page_url)
        url = page.src('img[alt^="strip for"]')
        return CrawlerImage(url)
