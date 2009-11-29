from comics.aggregator.crawler import BaseComicCrawler
from comics.meta.base import BaseComicMeta

class ComicMeta(BaseComicMeta):
    name = 'The Unspeakable Vault (of Doom)'
    language = 'en'
    url = 'http://www.macguff.fr/goomi/unspeakable/'
    history_capable_days = 180
    time_zone = 1
    rights = 'Francois Launet'

class ComicCrawler(BaseComicCrawler):
    def crawl(self):
        feed = self.parse_feed(
            'http://www.macguff.fr/goomi/unspeakable/rss.xml')
        for entry in feed.for_day(self.pub_date):
            if entry.title.startswith('Strip #'):
                self.url = entry.content0.src('img')
                self.title = entry.summary.text('')
