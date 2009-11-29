from comics.aggregator.crawler import BaseComicCrawler
from comics.meta.base import BaseComicMeta

class ComicMeta(BaseComicMeta):
    name = 'This is Historic Times'
    language = 'en'
    url = 'http://www.thisishistorictimes.com/'
    start_date = '2006-01-01'
    history_capable_days = 60
    time_zone = -8
    rights = 'Terrence Nowicki, Jr.'

class ComicCrawler(BaseComicCrawler):
    def crawl(self):
        feed = self.parse_feed('http://thisishistorictimes.com/feed/')
        for entry in feed.for_day(self.pub_date):
            self.title = entry.title
            page = self.parse_page(entry.link)
            self.url = page.src('img[src*="/wp-content/uploads/"]')
