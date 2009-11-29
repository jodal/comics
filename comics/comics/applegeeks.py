from comics.aggregator.crawler import BaseComicCrawler
from comics.meta.base import BaseComicMeta

class ComicMeta(BaseComicMeta):
    name = 'AppleGeeks'
    language = 'en'
    url = 'http://www.applegeeks.com/'
    start_date = '2003-01-01'
    history_capable_days = 30
    schedule = 'Mo,Th'
    time_zone = -5
    rights = 'Mohammad Haque & Ananth Panagariya'

class ComicCrawler(BaseComicCrawler):
    def crawl(self):
        feed = self.parse_feed('http://www.applegeeks.com/rss/?cat=comic')
        for entry in feed.for_day(self.pub_date):
            self.url = entry.summary.src('img').replace('thumb.gif', '.jpg')
            self.title = entry.title
