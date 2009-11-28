from comics.aggregator.crawler import BaseComicCrawler
from comics.meta.base import BaseComicMeta

class ComicMeta(BaseComicMeta):
    name = 'Player vs Player'
    language = 'en'
    url = 'http://www.pvponline.com/'
    start_date = '1998-05-04'
    history_capable_days = 10
    schedule = 'Mo,Tu,We,Th,Fr'
    time_zone = -6
    rights = 'Scott R. Kurtz'

class ComicCrawler(BaseComicCrawler):
    def crawl(self):
        self.parse_feed('http://feedproxy.google.com/pvponline')

        for entry in self.feed.entries:
            if self.timestamp_to_date(entry.updated_parsed) == self.pub_date:
                self.title = entry.title
                pieces = entry.summary.split('"')
                for i, piece in enumerate(pieces):
                    if (piece.count('src=') and pieces[i + 1].startswith(
                        'http://www.pvponline.com/comics/pvp')):
                        self.url = pieces[i + 1]
                        return
