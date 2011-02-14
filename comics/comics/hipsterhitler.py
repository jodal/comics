from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.meta.base import MetaBase

class Meta(MetaBase):
    name = 'Hipster Hitler'
    language = 'en'
    url = 'http://www.hipsterhitler.com/'
    start_date = '2010-08-01'
    rights = 'JC & APK'

class Crawler(CrawlerBase):
    history_capable_days = 40
    schedule = None
    time_zone = 0

    def crawl(self, pub_date):
        feed = self.parse_feed('http://hipsterhitler.com/feed/')
        for entry in feed.for_date(pub_date):
            page = self.parse_page(entry.link)
            url = page.src('img[src*="/wp-content/webcomic/"]')
            title = entry.title
            return CrawlerImage(url, title)
