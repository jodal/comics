from comics.crawler.base import BaseComicCrawler
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
    def _get_url(self):
        self.parse_feed('http://www.whattheduck.net/strip/rss.xml')

        for entry in self.feed.entries:
            if (self.timestamp_to_date(entry.updated_parsed) == self.pub_date
                and entry.enclosures[0].type.startswith('image')
                and entry.title.startswith('WTD')):
                self.title = entry.title
                self.url = entry.enclosures[0].href
                return
