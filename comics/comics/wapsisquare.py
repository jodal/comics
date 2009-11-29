from comics.aggregator.crawler import BaseComicCrawler
from comics.meta.base import BaseComicMeta

class ComicMeta(BaseComicMeta):
    name = 'Wapsi Square'
    language = 'en'
    url = 'http://wapsisquare.com/'
    start_date = '2001-09-09'
    history_capable_days = 14
    schedule = 'Mo,Tu,We,Th,Fr'
    rights = 'Paul Taylor'

class ComicCrawler(BaseComicCrawler):
    def crawl(self):
        feed = self.parse_feed('http://wapsisquare.com/feed/')
        for entry in feed.for_date(self.pub_date):
            self.url = entry.summary.src('img')
            self.title = entry.title
