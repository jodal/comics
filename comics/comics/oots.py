from comics.crawler.base import BaseComicCrawler
from comics.meta.base import BaseComicMeta

class ComicMeta(BaseComicMeta):
    name = 'The Order of the Stick'
    language = 'en'
    url = 'http://www.giantitp.com/'
    start_date = '2003-09-30'
    history_capable_days = 1
    schedule = 'Mo,We,Fr'
    time_zone = -5
    rights = 'Rich Burlew'

class ComicCrawler(BaseComicCrawler):
    def _get_url(self):
        self.parse_feed('http://www.giantitp.com/comics/oots.rss')
        if len(self.feed.entries):
            entry = self.feed.entries[0]
            self.title = entry.title
            page = self.parse_page(entry.link)
            self.url = page.src('img[src*="/comics/images/"]')
