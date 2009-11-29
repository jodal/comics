from comics.aggregator.crawler import BaseComicCrawler
from comics.meta.base import BaseComicMeta

class ComicMeta(BaseComicMeta):
    name = 'Bizarro'
    language = 'no'
    url = 'http://underholdning.no.msn.com/tegneserier/bizarro/'
    start_date = '1985-01-01'
    history_capable_days = 12
    schedule = 'Mo,Tu,We,Th,Fr,Sa,Su'
    time_zone = 1
    rights = 'Dan Piraro'

class ComicCrawler(BaseComicCrawler):
    def crawl(self):
        feed = self.parse_feed(
            'http://underholdning.no.msn.com/rss/bizarro.aspx')
        for entry in feed.for_day(self.pub_date):
            self.url = entry.enclosures[0].href
