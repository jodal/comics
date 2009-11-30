from comics.aggregator.crawler import BaseComicCrawler
from comics.meta.base import BaseComicMeta

class ComicMeta(BaseComicMeta):
    name = 'Nedroid'
    language = 'en'
    url = 'http://www.nedroid.com/'
    start_date = '2006-04-24'
    history_capable_days = 10
    schedule = 'Mo,Tu,We,Th,Fr,Sa,Su'
    time_zone = -5
    rights = 'Anthony Clark'

class ComicCrawler(BaseComicCrawler):
    def crawl(self):
        feed = self.parse_feed('http://nedroid.com/feed/')
        for entry in feed.for_date(self.pub_date):
            if 'Comic' in entry.tags:
                self.title = entry.title
                self.url = entry.summary.src('img')
                self.text = entry.summary.title('img')
