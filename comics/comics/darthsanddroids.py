from comics.crawler.base import BaseComicCrawler
from comics.crawler.meta import BaseComicMeta

class ComicMeta(BaseComicMeta):
    name = 'Darths & Droids'
    language = 'en'
    url = 'http://darthsanddroids.net/'
    start_date = '2007-09-14'
    history_capable_days = 14
    time_zone = -8
    rights = 'The Comic Irregulars'

class ComicCrawler(BaseComicCrawler):
    def _get_url(self):
        self.parse_feed('http://darthsanddroids.net/rss.xml')

        for entry in self.feed.entries:
            if (self.timestamp_to_date(entry.updated_parsed) == self.pub_date
                and entry.title.startswith('Episode')):
                self.title = entry.title
                pieces = entry.summary.split('"')
                for i, piece in enumerate(pieces):
                    if piece.count('src='):
                        self.url = pieces[i + 1]
                        return
