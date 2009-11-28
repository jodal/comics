from comics.crawler.base import BaseComicCrawler
from comics.meta.base import BaseComicMeta

class ComicMeta(BaseComicMeta):
    name = 'AmazingSuperPowers'
    language = 'en'
    url = 'http://www.amazingsuperpowers.com/'
    start_date = '2007-09-24'
    history_capable_days = 21
    schedule = 'Mo,Th'
    rights = 'Wes & Tony'

class ComicCrawler(BaseComicCrawler):
    def _get_url(self):
        self.parse_feed('http://www.amazingsuperpowers.com/category/comics/feed/')

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
