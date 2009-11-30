from comics.aggregator.crawler import BaseComicCrawler
from comics.meta.base import BaseComicMeta

class ComicMeta(BaseComicMeta):
    name = 'Darths & Droids'
    language = 'en'
    url = 'http://darthsanddroids.net/'
    start_date = '2007-09-14'
    history_capable_days = 14
    time_zone = -8
    rights = 'The Comic Irregulars'

class ComicCrawler(BaseComicCrawler):
    def crawl(self):
        feed = self.parse_feed('http://darthsanddroids.net/rss.xml')
        for entry in feed.for_date(self.pub_date):
            if entry.title.startswith('Episode'):
                self.url = entry.summary.src('img')
                self.title = entry.title
