from comics.crawler.base import BaseComicCrawler
from comics.meta.base import BaseComicMeta

class ComicMeta(BaseComicMeta):
    name = 'Nedroid'
    language = 'en'
    url = 'http://www.nedroid.com/'
    start_date = '2006-04-24'
    history_capable_days = 10
    schedule = 'Mo,Tu,We,Th,Fr,Sa,Su'
    time_zone = -5
    rights = 'Anthony Clark'

class ComicCrawler(BaseComicCrawler):
    def _get_url(self):
        self.parse_feed('http://nedroid.com/feed/atom/')

        for entry in self.feed.entries:
            if self.timestamp_to_date(entry.updated_parsed) == self.pub_date:
                self.title = entry.title
                pieces = entry.summary.split('"')
                for i, piece in enumerate(pieces):
                    if piece.count('src='):
                        self.url = pieces[i + 1]
                    if piece.count('title='):
                        self.text = pieces[i + 1]
                    if self.url and self.text:
                        return
