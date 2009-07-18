from comics.crawler.crawlers import BaseComicCrawler
from comics.crawler.meta import BaseComicMeta

class ComicMeta(BaseComicMeta):
    name = 'Saturday Morning Breakfast Cereal'
    language = 'en'
    url = 'http://www.smbc-comics.com/'
    start_date = '2002-09-05'
    history_capable_days = 10
    schedule = 'Mo,Tu,We,Th,Fr,Sa,Su'
    time_zone = -8
    rights = 'Zach Weiner'

class ComicCrawler(BaseComicCrawler):
    def _get_url(self):
        self.parse_feed('http://www.smbc-comics.com/rss.php')

        for entry in self.feed.entries:
            if self.timestamp_to_date(entry.updated_parsed) == self.pub_date:
                pieces = entry.summary.split('"')
                for i, piece in enumerate(pieces):
                    if piece.count('src='):
                        self.url = pieces[i + 1]
                        return
