from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.meta.base import MetaBase

class Meta(MetaBase):
    name = 'Axe Cop'
    language = 'en'
    url = 'http://www.axecop.com/'
    start_date = '2010-01-02'
    rights = 'Ethan Nicolle'

class Crawler(CrawlerBase):
    history_capable_days = 60
    time_zone = -8

    def crawl(self, pub_date):
        feed = self.parse_feed('http://axecop.com/index.php/achome/rss_2.0/')
        for entry in feed.for_date(pub_date):
            page_url = entry.link
            page = self.parse_page(page_url)

            url = page.src('img[src*="/images/uploads/axecop"]')
            return CrawlerImage(url)
