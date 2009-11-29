from comics.aggregator.crawler import BaseComicCrawler
from comics.meta.base import BaseComicMeta

class ComicMeta(BaseComicMeta):
    name = 'AmazingSuperPowers'
    language = 'en'
    url = 'http://www.amazingsuperpowers.com/'
    start_date = '2007-09-24'
    history_capable_days = 21
    schedule = 'Mo,Th'
    rights = 'Wes & Tony'

class ComicCrawler(BaseComicCrawler):
    def crawl(self):
        feed = self.parse_feed(
            'http://www.amazingsuperpowers.com/category/comics/feed/')
        for entry in feed.for_date(self.pub_date):
            self.url = entry.summary.src('img')
            self.title = entry.title
            self.text = entry.summary.title('img')
