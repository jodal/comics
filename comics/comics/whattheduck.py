from comics.aggregator.crawler import BaseComicCrawler
from comics.meta.base import BaseComicMeta

class ComicMeta(BaseComicMeta):
    name = 'What the Duck'
    language = 'en'
    url = 'http://www.whattheduck.net/'
    start_date = '2006-07-01'
    history_capable_days = 7
    schedule = 'Mo,Tu,We,Th,Fr'
    rights = 'Aaron Johnson'

class ComicCrawler(BaseComicCrawler):
    def crawl(self):
        feed = self.parse_feed('http://www.whattheduck.net/strip/rss.xml')
        for entry in feed.for_day(self.pub_date):
            if (entry.enclosures[0].type.startswith('image')
                    and entry.title.startswith('WTD')):
                self.url = entry.enclosures[0].href
                self.title = entry.title
