from comics.crawler.crawlers import BaseComicCrawler
from comics.crawler.meta import BaseComicMeta

class ComicMeta(BaseComicMeta):
    name = 'AppleGeeks Lite'
    language = 'en'
    url = 'http://www.applegeeks.com/'
    start_date = '2006-04-18'
    history_capable_days = 30
    schedule = 'Mo,We,Fr'
    time_zone = -5
    rights = 'Mohammad Haque & Ananth Panagariya'

class ComicCrawler(BaseComicCrawler):
    def _get_url(self):
        self.parse_feed('http://www.applegeeks.com/rss/?cat=lite')

        for entry in self.feed.entries:
            if self.timestamp_to_date(entry.updated_parsed) == self.pub_date:
                self.title = entry.title.replace('AG Lite - ', '')
                pieces = entry['summary'].split('"')
                for i, piece in enumerate(pieces):
                    if piece.count('src='):
                        self.url = pieces[i + 1]
                        return
