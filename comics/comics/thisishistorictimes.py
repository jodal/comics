from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.meta.base import MetaBase

class Meta(MetaBase):
    name = 'This is Historic Times'
    language = 'en'
    url = 'http://www.thisishistorictimes.com/'
    start_date = '2006-01-01'
    rights = 'Terrence Nowicki, Jr.'

class Crawler(CrawlerBase):
    history_capable_days = 60
    time_zone = -8

    def crawl(self, pub_date):
        feed = self.parse_feed('http://thisishistorictimes.com/feed/')
        for entry in feed.for_date(pub_date):
            page = self.parse_page(entry.link)
            url = page.src('img[src*="/wp-content/uploads/"]')
            title = entry.title
            return CrawlerImage(url, title)
