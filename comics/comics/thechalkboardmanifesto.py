from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.meta.base import MetaBase

class Meta(MetaBase):
    name = 'The Chalkboard Manifesto'
    language = 'en'
    url = 'http://www.chalkboardmanifesto.com/'
    start_date = '2005-05-01'
    rights = 'Shawn McDonald'

class Crawler(CrawlerBase):
    history_capable_days = 40
    schedule = 'Mo,We,Fr'

    def crawl(self, pub_date):
        feed = self.parse_feed(
            'http://feeds.feedburner.com/TheChalkboardManifesto')
        for entry in feed.for_date(pub_date):
            url = entry.summary.src('img[alt="comic"]')
            title = entry.title
            return CrawlerImage(url, title)
