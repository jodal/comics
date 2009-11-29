from comics.aggregator.crawler import BaseComicCrawler
from comics.meta.base import BaseComicMeta

class ComicMeta(BaseComicMeta):
    name = 'xkcd'
    language = 'en'
    url = 'http://www.xkcd.com/'
    start_date = '2005-05-29'
    history_capable_days = 10
    schedule = 'Mo,We,Fr'
    time_zone = -5
    rights = 'Randall Munroe, CC BY-NC 2.5'

class ComicCrawler(BaseComicCrawler):
    def crawl(self):
        feed = self.parse_feed('http://www.xkcd.com/rss.xml')
        for entry in feed.for_day(self.pub_date):
            self.url = entry.summary.src('img')
            self.title = entry.title
            self.text = entry.summary.alt('img')
