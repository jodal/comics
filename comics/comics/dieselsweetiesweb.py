from comics.aggregator.crawler import BaseComicCrawler
from comics.meta.base import BaseComicMeta

class ComicMeta(BaseComicMeta):
    name = 'Diesel Sweeties (web)'
    language = 'en'
    url = 'http://www.dieselsweeties.com/'
    start_date = '2000-01-01'
    history_capable_date = '2000-01-01'
    schedule = 'Mo,Tu,We,Th,Fr'
    time_zone = -5
    rights = 'Richard Stevens'

class ComicCrawler(BaseComicCrawler):
    def crawl(self):
        feed = self.parse_feed('http://www.dieselsweeties.com/ds-unifeed.xml')
        for entry in feed.for_day(self.pub_date):
            if entry.title.startswith('DS Web:'):
                self.url = entry.summary.src('img')
                self.title = entry.title.replace('DS Web: ', '').strip()
                self.text = entry.summary.alt('img')
