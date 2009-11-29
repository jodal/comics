from comics.aggregator.crawler import BaseComicCrawler
from comics.meta.base import BaseComicMeta

class ComicMeta(BaseComicMeta):
    name = 'Garfield minus Garfield'
    language = 'en'
    url = 'http://garfieldminusgarfield.tumblr.com/'
    history_capable_days = 30
    schedule = 'Mo,Tu,We,Th,Fr'
    time_zone = -4
    rights = 'Travors'

class ComicCrawler(BaseComicCrawler):
    def crawl(self):
        feed = self.parse_feed('http://garfieldminusgarfield.tumblr.com/rss')
        for entry in feed.for_day(self.pub_date):
            self.url = entry.summary.src('img')
