from comics.aggregator.crawler import BaseComicCrawler
from comics.meta.base import BaseComicMeta

class ComicMeta(BaseComicMeta):
    name = 'Geek and Poke'
    language = 'en'
    url = 'http://www.geekandpoke.com/'
    start_date = '2006-08-22'
    history_capable_days = 32
    schedule = 'Mo,Tu,We,Th,Fr,Sa,Su'
    time_zone = 1
    rights = 'Oliver Widder, CC BY-ND 2.0'

class ComicCrawler(BaseComicCrawler):
    def crawl(self):
        feed = self.parse_feed(
            'http://geekandpoke.typepad.com/geekandpoke/atom.xml')
        for entry in feed.for_date(self.pub_date):
            self.url = entry.content0.src('img.asset-image')
            self.title = entry.title
            self.text = entry.content0.alt('img.asset-image')
