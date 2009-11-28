from comics.aggregator.crawler import BaseComicCrawler
from comics.meta.base import BaseComicMeta

class ComicMeta(BaseComicMeta):
    name = 'Boy on a Stick and Slither'
    language = 'en'
    url = 'http://www.boasas.com/'
    start_date = '1998-01-01'
    history_capable_days = 14
    schedule = 'Mo,We,Fr'
    time_zone = -5
    rights = 'Steven L. Cloud'

class ComicCrawler(BaseComicCrawler):
    def crawl(self):
        self.parse_feed('http://www.boasas.com/boasas_rss.xml')

        for entry in self.feed.entries:
            if self.timestamp_to_date(entry.updated_parsed) == self.pub_date:
                self.title = entry.title
                pieces = entry.summary.split('"')
                for i, piece in enumerate(pieces):
                    if piece.count('src='):
                        self.url = pieces[i + 1]
                    if self.url and self.text:
                        return
