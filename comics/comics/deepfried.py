from comics.aggregator.crawler import BaseComicCrawler
from comics.meta.base import BaseComicMeta

class ComicMeta(BaseComicMeta):
    name = 'Deep Fried'
    language = 'en'
    url = 'http://www.whatisdeepfried.com/'
    start_date = '2001-09-16'
    history_capable_days = 14
    schedule = 'Mo,Tu,We,Th,Fr,Sa'
    time_zone = -5
    rights = 'Jason Yungbluth'

class ComicCrawler(BaseComicCrawler):
    def crawl(self):
        feed = self.parse_feed('http://www.whatisdeepfried.com/feed/')
        for entry in feed.for_date(self.pub_date):
            self.url = entry.summary.src('img')
            self.title = entry.title
