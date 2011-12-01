from comics.aggregator.crawler import CrawlerBase, CrawlerImage
from comics.meta.base import MetaBase

class Meta(MetaBase):
    name = 'I Can Barely Draw'
    language = 'en'
    url = 'http://www.icanbarelydraw.com/comic/'
    start_date = '2011-08-05'
    rights = 'Group effort, CC BY-NC-ND 3.0'

class Crawler(CrawlerBase):
    history_capable_days = 30
    schedule = 'Mo,We,Fr'
    time_zone = -5

    def crawl(self, pub_date):
        feed = self.parse_feed('http://www.icanbarelydraw.com/comic/feed')
        for entry in feed.for_date(pub_date):
            url = entry.summary.src('img[src*="/comics-rss/"]')
            title = entry.title
            return CrawlerImage(url, title)
