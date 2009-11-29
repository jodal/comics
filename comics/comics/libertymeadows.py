from comics.aggregator.crawler import BaseComicCrawler
from comics.meta.base import BaseComicMeta

class ComicMeta(BaseComicMeta):
    name = 'Liberty Meadows'
    language = 'en'
    url = 'http://www.creators.com/comics/liberty-meadows.html'
    start_date = '1997-03-30'
    end_date = '2001-12-31'
    history_capable_days = 19
    schedule = 'Mo,Tu,We,Th,Fr,Sa,Su'
    time_zone = -8
    rights = 'Frank Cho'

class ComicCrawler(BaseComicCrawler):
    def crawl(self):
        feed = self.parse_feed(
            'http://www.creators.com/comics/liberty-meadows.rss')
        for entry in feed.for_date(self.pub_date):
            page = self.parse_page(entry.link)
            self.url = page.src('img[src*="_thumb"]').replace('thumb', 'image')
