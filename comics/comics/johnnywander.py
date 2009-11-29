from comics.aggregator.crawler import BaseComicCrawler
from comics.meta.base import BaseComicMeta

class ComicMeta(BaseComicMeta):
    name = 'Johnny Wander'
    language = 'en'
    url = 'http://www.johnnywander.com/'
    start_date = '2008-09-30'
    history_capable_days = 40
    schedule = 'Tu,Th'
    time_zone = -8
    rights = 'Yuko Ota & Ananth Panagariya'

class ComicCrawler(BaseComicCrawler):
    def crawl(self):
        feed = self.parse_feed('http://www.johnnywander.com/feed')
        for entry in feed.for_day(self.pub_date):
            self.url = entry.summary.src('img')
            self.title = entry.title
            self.text = entry.summary.title('img')
