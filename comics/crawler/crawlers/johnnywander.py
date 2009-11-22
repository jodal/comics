from comics.crawler.base import BaseComicCrawler
from comics.crawler.meta import BaseComicMeta

class ComicMeta(BaseComicMeta):
    name = 'Johnny Wander'
    language = 'en'
    url = 'http://www.johnnywander.com/'
    start_date = '2008-09-30'
    history_capable_days = 40
    schedule = 'Tu,Th'
    time_zone = -8
    rights = 'Yuko Ota & Ananth Panagariya'

class ComicCrawler(BaseComicCrawler):
    def _get_url(self):
        self.parse_feed('http://www.johnnywander.com/feed')

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
