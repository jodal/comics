from comics.aggregator.crawler import BaseComicCrawler
from comics.meta.base import BaseComicMeta

class ComicMeta(BaseComicMeta):
    name = 'MegaTokyo'
    language = 'en'
    url = 'http://www.megatokyo.com/'
    start_date = '2000-08-14'
    history_capable_days = 30
    schedule = 'Mo,We,Fr'
    time_zone = -5
    rights = 'Fred Gallagher & Rodney Caston'

class ComicCrawler(BaseComicCrawler):
    def crawl(self):
        feed = self.parse_feed('http://www.megatokyo.com/rss/megatokyo.xml')
        for entry in feed.for_day(self.pub_date):
            if entry.title.startswith('Comic ['):
                self.title = entry.title.split('"')[1]
                page = self.parse_page(entry.link)
                self.url = page.src('img[src*="/strips/"]')
