from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.meta.base import MetaBase

class Meta(MetaBase):
    name = 'Bug'
    language = 'en'
    url = 'http://www.bugcomic.com/'
    start_date = '2009-10-19'
    rights = 'Adam Huber'

class Crawler(CrawlerBase):
    history_capable_days = 15
    schedule = 'Mo,Tu,We,Th,Fr'
    time_zone = -5

    def crawl(self, pub_date):
        feed = self.parse_feed('http://www.bugcomic.com/feed/')
        for entry in feed.for_date(pub_date):
            url = entry.summary.src('img[src*="/comics-rss/"]')
            if url is None:
                return
            url = url.replace('-rss', '')
            title = entry.title
            return CrawlerImage(url, title)
