from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.meta.base import MetaBase

class Meta(MetaBase):
    name = 'Buttersafe'
    language = 'en'
    url = 'http://buttersafe.com/'
    start_date = '2007-04-03'
    rights = 'Alex Culang & Raynato Castro'

class Crawler(CrawlerBase):
    history_capable_days = 90
    time_zone = -7

    def crawl(self, pub_date):
        feed = self.parse_feed(
            'http://feeds.feedburner.com/Buttersafe?format=xml')
        for entry in feed.for_date(pub_date):
            url = entry.summary.src('img[src*="/comics/"]')
            if not url:
                continue
            url = url.replace('/rss/', '/').replace('RSS.jpg', '.jpg')
            title = entry.title
            return CrawlerImage(url, title)
