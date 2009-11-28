from comics.aggregator.crawler import BaseComicCrawler
from comics.meta.base import BaseComicMeta

class ComicMeta(BaseComicMeta):
    name = 'Little Gamers'
    language = 'en'
    url = 'http://www.little-gamers.com/'
    start_date = '2000-12-01'
    history_capable_date = '2000-12-01'
    schedule = 'Mo,Tu,We,Th,Fr'
    time_zone = 1
    rights = 'Christian Fundin & Pontus Madsen'

class ComicCrawler(BaseComicCrawler):
    def crawl(self):
        self.parse_feed('http://www.little-gamers.com/category/comic/feed')

        for entry in self.feed.entries:
            if self.timestamp_to_date(entry.updated_parsed) == self.pub_date:
                self.title = entry.title
                pieces = entry.summary.split('"')
                for i, piece in enumerate(pieces):
                    if piece.count('src='):
                        self.url = pieces[i + 1]
                        return
