from comics.aggregator.crawler import BaseComicCrawler
from comics.meta.base import BaseComicMeta

class ComicMeta(BaseComicMeta):
    name = 'White Ninja'
    language = 'en'
    url = 'http://www.whiteninjacomics.com/'
    start_date = '2002-01-01'
    history_capable_days = 60
    time_zone = -6
    rights = 'Scott Bevan & Kent Earle'

class ComicCrawler(BaseComicCrawler):
    def crawl(self):
        feed = self.parse_feed(
            'http://www.whiteninjacomics.com/rss/z-latest.xml')
        for entry in feed.for_date(self.pub_date):
            self.title = entry.title.split(' - ')[0]
            page = self.parse_page(entry.link)
            page.remove('img[src*="/images/comics/t-"]')
            self.url = page.src('img[src*="/images/comics/"]')
