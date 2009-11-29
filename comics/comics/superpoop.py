from comics.aggregator.crawler import BaseComicCrawler
from comics.meta.base import BaseComicMeta

class ComicMeta(BaseComicMeta):
    name = 'Superpoop'
    language = 'en'
    url = 'http://www.superpoop.com/'
    start_date = '2008-01-01'
    history_capable_days = 30
    schedule = 'Mo,Tu,We,Th'
    time_zone = -5
    rights = 'Drew'

class ComicCrawler(BaseComicCrawler):
    def crawl(self):
        feed = self.parse_feed('http://www.superpoop.com/rss/rss.php')
        for entry in feed.for_day(self.pub_date):
            self.url = entry.summary.src('img[src$=".jpg"]')
            self.title = entry.title
