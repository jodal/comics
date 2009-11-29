from comics.aggregator.crawler import BaseComicCrawler
from comics.meta.base import BaseComicMeta

class ComicMeta(BaseComicMeta):
    name = 'Saturday Morning Breakfast Cereal'
    language = 'en'
    url = 'http://www.smbc-comics.com/'
    start_date = '2002-09-05'
    history_capable_days = 10
    schedule = 'Mo,Tu,We,Th,Fr,Sa,Su'
    time_zone = -8
    rights = 'Zach Weiner'

class ComicCrawler(BaseComicCrawler):
    def crawl(self):
        feed = self.parse_feed('http://www.smbc-comics.com/rss.php')
        for entry in feed.for_date(self.pub_date):
            self.url = entry.summary.src('img')
