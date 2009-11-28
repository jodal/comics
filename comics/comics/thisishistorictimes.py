from comics.crawler.base import BaseComicCrawler
from comics.crawler.meta import BaseComicMeta

class ComicMeta(BaseComicMeta):
    name = 'This is Historic Times'
    language = 'en'
    url = 'http://www.thisishistorictimes.com/'
    start_date = '2006-01-01'
    history_capable_days = 60
    time_zone = -8
    rights = 'Terrence Nowicki, Jr.'

class ComicCrawler(BaseComicCrawler):
    def _get_url(self):
        self.parse_feed('http://thisishistorictimes.com/feed/')
        for entry in self.feed.entries:
            if self.timestamp_to_date(entry.updated_parsed) == self.pub_date:
                self.title = entry.title
                page = self.parse_page(entry.link)
                self.url = page.src('img[src*="/wp-content/uploads/"]')
