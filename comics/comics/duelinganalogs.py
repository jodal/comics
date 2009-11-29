from comics.aggregator.crawler import BaseComicCrawler
from comics.meta.base import BaseComicMeta

class ComicMeta(BaseComicMeta):
    name = 'Dueling Analogs'
    language = 'en'
    url = 'http://www.duelinganalogs.com/'
    start_date = '2005-11-17'
    history_capable_days = 35
    schedule = 'Mo,Th'
    time_zone = -7
    rights = 'Steve Napierski'

class ComicCrawler(BaseComicCrawler):
    def crawl(self):
        feed = self.parse_feed('http://feeds2.feedburner.com/DuelingAnalogs')
        for entry in feed.for_day(self.pub_date):
            self.url = entry.summary.src('img[src*="/comics/"]')
            self.title = entry.title
