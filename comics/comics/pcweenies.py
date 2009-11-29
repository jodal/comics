from comics.aggregator.crawler import BaseComicCrawler
from comics.meta.base import BaseComicMeta

class ComicMeta(BaseComicMeta):
    name = 'The PC Weenies'
    language = 'en'
    url = 'http://www.pcweenies.com/'
    start_date = '1998-10-21'
    history_capable_days = 10
    schedule = 'Mo,We,Fr'
    time_zone = -8
    rights = 'Krishna M. Sadasivam'

class ComicCrawler(BaseComicCrawler):
    def crawl(self):
        feed = self.parse_feed('http://www.pcweenies.com/feed/')
        for entry in feed.for_day(self.pub_date):
            if entry.has_tag('Comic'):
                self.title = entry.title
                self.url = entry.content0.src(u'img')
