from comics.aggregator.crawler import BaseComicCrawler
from comics.meta.base import BaseComicMeta

class ComicMeta(BaseComicMeta):
    name = 'Three Panel Soul'
    language = 'en'
    url = 'http://www.threepanelsoul.com/'
    start_date = '2006-11-05'
    history_capable_days = 180
    time_zone = -5
    rights = 'Ian McConville & Matt Boyd'

class ComicCrawler(BaseComicCrawler):
    def crawl(self):
        feed = self.parse_feed('http://www.rsspect.com/rss/threeps.xml')
        for entry in feed.for_day(self.pub_date):
            self.url = entry.summary.src('img')
            self.title = entry.title
            self.text = entry.summary.alt('img')
