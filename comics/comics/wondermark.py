from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.meta.base import MetaBase

class Meta(MetaBase):
    name = 'Wondermark'
    language = 'en'
    url = 'http://wondermark.com/'
    start_date = '2003-04-25'
    rights = 'David Malki'

class Crawler(CrawlerBase):
    history_capable_days = 28
    schedule = 'Tu,Fr'
    time_zone = -8

    def crawl(self, pub_date):
        feed_url = 'http://feeds.feedburner.com/wondermark'
        feed = self.parse_feed(feed_url)
        for entry in feed.for_date(pub_date):
            url = entry.content0.src('img[src*="/c/"]')
            title = entry.title
            text = entry.content0.alt('img[src*="/c/"]')
            if url is not None:
                return CrawlerImage(url, title, text)
