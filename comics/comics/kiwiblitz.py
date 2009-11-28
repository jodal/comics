from comics.crawler.base import BaseComicCrawler
from comics.meta.base import BaseComicMeta

class ComicMeta(BaseComicMeta):
    name = 'Kiwiblitz'
    language = 'en'
    url = 'http://www.kiwiblitz.com/'
    start_date = '2009-04-18'
    history_capable_days = 32
    schedule = 'Mo,We'
    time_zone = -8
    rights = 'Mary Cagle'

class ComicCrawler(BaseComicCrawler):
    def _get_url(self):
        self.parse_feed('http://www.kiwiblitz.com/?feed=rss2')

        for entry in self.feed.entries:
            if self.timestamp_to_date(entry.updated_parsed) == self.pub_date:
                pieces = entry.summary.split('"')
                for i, piece in enumerate(pieces):
                    if (piece.count('src=') and pieces[i + 1].startswith(
                            'http://www.kiwiblitz.com/comics/')):
                        self.url = pieces[i + 1]
                    if piece.count('alt='):
                        self.title = pieces[i + 1]
                    if self.url and self.title:
                        return
