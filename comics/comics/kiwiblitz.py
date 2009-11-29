from comics.aggregator.crawler import BaseComicCrawler
from comics.meta.base import BaseComicMeta

class ComicMeta(BaseComicMeta):
    name = 'Kiwiblitz'
    language = 'en'
    url = 'http://www.kiwiblitz.com/'
    start_date = '2009-04-18'
    history_capable_days = 32
    schedule = 'Mo,We'
    time_zone = -8
    rights = 'Mary Cagle'

class ComicCrawler(BaseComicCrawler):
    def crawl(self):
        feed = self.parse_feed('http://www.kiwiblitz.com/?feed=rss2')
        for entry in feed.for_date(self.pub_date):
            self.url = entry.summary.src('img[src*="/comics/"]')
            self.title = entry.summary.alt('img[src*="/comics/"]')
