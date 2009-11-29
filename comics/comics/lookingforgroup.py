from comics.aggregator.crawler import BaseComicCrawler
from comics.meta.base import BaseComicMeta

class ComicMeta(BaseComicMeta):
    name = 'Looking For Group'
    language = 'en'
    url = 'http://lfgcomic.com/'
    start_date = '2006-11-06'
    history_capable_date = '2006-11-06'
    schedule = 'Mo,Th'
    time_zone = -5
    rights = 'Ryan Sohmer & Lar deSouza'

class ComicCrawler(BaseComicCrawler):
    def crawl(self):
        feed = self.parse_feed('http://feeds.feedburner.com/LookingForGroup')
        for entry in feed.for_day(self.pub_date):
            self.url = entry.summary.src('img[src*="lfgcomic.com"]')
            self.title = entry.title.replace('Looking For Group:', '').strip()
