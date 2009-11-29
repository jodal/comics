from comics.aggregator.crawler import BaseComicCrawler
from comics.meta.base import BaseComicMeta

class ComicMeta(BaseComicMeta):
    name = 'PartiallyClips'
    language = 'en'
    url = 'http://www.partiallyclips.com/'
    start_date = '2002-01-01'
    history_capable_days = 10
    schedule = 'Tu'
    time_zone = -5
    rights = 'Robert T. Balder'

class ComicCrawler(BaseComicCrawler):
    def crawl(self):
        feed = self.parse_feed('http://www.partiallyclips.com/includes/rss.xml')
        for entry in feed.for_date(self.pub_date):
            self.url = entry.summary.src('img')
            self.title = entry.title.split(' - ')[0]
