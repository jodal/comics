from comics.aggregator.crawler import BaseComicCrawler
from comics.meta.base import BaseComicMeta

class ComicMeta(BaseComicMeta):
    name = 'GU Comics'
    language = 'en'
    url = 'http://www.gucomics.com/'
    start_date = '2000-07-10'
    history_capable_date = '2000-07-10'
    schedule = 'Mo,Tu,We,Th,Fr'
    time_zone = -8
    rights = 'Woody Hearn'

class ComicCrawler(BaseComicCrawler):
    def crawl(self):
        feed = self.parse_feed('http://www.gucomics.com/rss.xml')
        for entry in feed.for_day(self.pub_date):
            if entry.title.startswith('Comic:'):
                self.title = entry.summary.text('')
                page = self.parse_page(entry.link)
                self.url = page.src(
                    'img[src^="http://www.gucomics.com/comics/"]'
                    '[alt^="Comic for:"]')
