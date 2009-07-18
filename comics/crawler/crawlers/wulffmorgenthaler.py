from comics.crawler.crawlers import BaseComicCrawler
from comics.crawler.meta import BaseComicMeta

class ComicMeta(BaseComicMeta):
    name = 'Wulffmorgenthaler'
    language = 'en'
    url = 'http://www.wulffmorgenthaler.com/'
    start_date = '2001-01-01'
    history_capable_days = 10
    schedule = 'Mo,Tu,We,Th,Fr,Sa,Su'
    time_zone = 1
    rights = 'Mikael Wulff & Anders Morgenthaler'

class ComicCrawler(BaseComicCrawler):
    def _get_url(self):
        self.parse_feed('http://feeds.feedburner.com/wulffmorgenthaler')

        for entry in self.feed.entries:
            if self.timestamp_to_date(entry.updated_parsed) == self.pub_date:
                pieces = entry.summary.split('"')
                for i, piece in enumerate(pieces):
                    if piece.count('src='):
                        self.url = pieces[i + 1]
                        return
