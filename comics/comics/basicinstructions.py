from comics.aggregator.crawler import BaseComicCrawler
from comics.meta.base import BaseComicMeta

class ComicMeta(BaseComicMeta):
    name = 'Basic Instructions'
    language = 'en'
    url = 'http://www.basicinstructions.net/'
    start_date = '2006-07-01'
    history_capable_days = 100
    schedule = 'We,Su'
    time_zone = -7
    rights = 'Scott Meyer'

class ComicCrawler(BaseComicCrawler):
    def crawl(self):
        feed = self.parse_feed('http://www.basicinstructions.net/atom.xml')
        for entry in feed.for_day(self.pub_date):
            self.url = entry.content0.src('img[src*="/comics/"]', False)
            self.title = entry.title
