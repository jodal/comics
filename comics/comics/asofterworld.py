from comics.aggregator.crawler import BaseComicCrawler
from comics.meta.base import BaseComicMeta

class ComicMeta(BaseComicMeta):
    name = 'A Softer World'
    language = 'en'
    url = 'http://www.asofterworld.com/'
    start_date = '2003-02-07'
    history_capable_date = '2003-02-07'
    schedule = 'Mo,We,Fr'
    time_zone = -8
    rights = 'Joey Comeau, Emily Horne'

class ComicCrawler(BaseComicCrawler):
    def crawl(self):
        feed = self.parse_feed('http://www.rsspect.com/rss/asw.xml')
        for entry in feed.for_day(self.pub_date):
            if entry.link != 'http://www.asofterworld.com':
                self.url = entry.summary.src('img[src*="/clean/"]')
                self.title = entry.title
                self.text = entry.summary.title('img[src*="/clean/"]')
