from comics.aggregator.crawler import BaseComicCrawler
from comics.meta.base import BaseComicMeta

class ComicMeta(BaseComicMeta):
    name = 'Questionable Content'
    language = 'en'
    url = 'http://questionablecontent.net/'
    start_date = '2003-08-01'
    history_capable_date = '2003-08-01'
    schedule = 'Mo,Tu,We,Th,Fr'
    time_zone = -6
    rights = 'Jeph Jacques'

class ComicCrawler(BaseComicCrawler):
    def crawl(self):
        feed = self.parse_feed('http://www.questionablecontent.net/QCRSS.xml')
        for entry in feed.for_day(self.pub_date):
            self.url = entry.summary.src('img')
            self.title = entry.title
