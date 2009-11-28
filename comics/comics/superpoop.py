from comics.aggregator.crawler import BaseComicCrawler
from comics.meta.base import BaseComicMeta

class ComicMeta(BaseComicMeta):
    name = 'Superpoop'
    language = 'en'
    url = 'http://www.superpoop.com/'
    start_date = '2008-01-01'
    history_capable_days = 30
    schedule = 'Mo,Tu,We,Th'
    time_zone = -5
    rights = 'Drew'

class ComicCrawler(BaseComicCrawler):
    def _get_url(self):
        self.parse_feed('http://www.superpoop.com/rss/rss.php')

        for entry in self.feed.entries:
            if self.timestamp_to_date(entry.updated_parsed) == self.pub_date:
                self.title = entry.title
                pieces = entry.summary.split('"')
                for i, piece in enumerate(pieces):
                    if piece.count('src='):
                        self.url = pieces[i + 1]
                        return
