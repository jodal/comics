from comics.aggregator.crawler import BaseComicCrawler
from comics.meta.base import BaseComicMeta

class ComicMeta(BaseComicMeta):
    name = 'Player vs Player'
    language = 'en'
    url = 'http://www.pvponline.com/'
    start_date = '1998-05-04'
    history_capable_days = 10
    schedule = 'Mo,Tu,We,Th,Fr'
    time_zone = -6
    rights = 'Scott R. Kurtz'

class ComicCrawler(BaseComicCrawler):
    def crawl(self):
        feed = self.parse_feed('http://feeds.feedburner.com/Pvponline')
        for entry in feed.for_date(self.pub_date):
            self.url = entry.content0.src('img[src*="/comics/"]')
            self.title = entry.title
