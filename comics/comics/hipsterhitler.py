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
    time_zone = 0

    def crawl(self, pub_date):
        feed = self.parse_feed('http://hipsterhitler.com/feed/')
        for entry in feed.for_date(pub_date):
            url = entry.content0.src('img[src*="/wp-content/uploads/"]')
            title = entry.title
            return CrawlerImage(url, title)
