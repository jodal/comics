from comics.aggregator.crawler import BaseComicCrawler
from comics.meta.base import BaseComicMeta

class ComicMeta(BaseComicMeta):
    name = 'InkTank'
    language = 'en'
    url = 'http://www.inktank.com/'
    start_date = '2008-04-01'
    history_capable_days = 32
    schedule = 'Mo,We,Fr'
    time_zone = -8
    rights = 'Barry T. Smith'

class ComicCrawler(BaseComicCrawler):
    def crawl(self):
        feed = self.parse_feed('http://feeds.feedburner.com/inktank/HstZ')
        for entry in feed.for_date(self.pub_date):
            self.url = entry.summary.src('img[src*="/comics-rss/"]')
            self.title = entry.title
