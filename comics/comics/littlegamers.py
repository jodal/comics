from comics.aggregator.crawler import BaseComicCrawler
from comics.meta.base import BaseComicMeta

class ComicMeta(BaseComicMeta):
    name = 'Little Gamers'
    language = 'en'
    url = 'http://www.little-gamers.com/'
    start_date = '2000-12-01'
    history_capable_date = '2000-12-01'
    schedule = 'Mo,Tu,We,Th,Fr'
    time_zone = 1
    rights = 'Christian Fundin & Pontus Madsen'

class ComicCrawler(BaseComicCrawler):
    def crawl(self):
        feed = self.parse_feed(
            'http://www.little-gamers.com/category/comic/feed')
        for entry in feed.for_date(self.pub_date):
            self.url = entry.summary.src('img')
            self.title = entry.title
