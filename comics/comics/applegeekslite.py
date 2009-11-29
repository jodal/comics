from comics.aggregator.crawler import BaseComicCrawler
from comics.meta.base import BaseComicMeta

class ComicMeta(BaseComicMeta):
    name = 'AppleGeeks Lite'
    language = 'en'
    url = 'http://www.applegeeks.com/'
    start_date = '2006-04-18'
    history_capable_days = 30
    schedule = 'Mo,We,Fr'
    time_zone = -5
    rights = 'Mohammad Haque & Ananth Panagariya'

class ComicCrawler(BaseComicCrawler):
    def crawl(self):
        feed = self.parse_feed('http://www.applegeeks.com/rss/?cat=lite')
        for entry in feed.for_day(self.pub_date):
            self.url = entry.summary.src('img')
            self.title = entry.title.replace('AG Lite - ', '')
