from comics.aggregator.crawler import BaseComicCrawler
from comics.meta.base import BaseComicMeta

class ComicMeta(BaseComicMeta):
    name = 'A Softer World'
    language = 'en'
    url = 'http://www.asofterworld.com/'
    start_date = '2003-02-07'
    history_capable_date = '2003-02-07'
    schedule = 'Mo,We,Fr'
    time_zone = -8
    rights = 'Joey Comeau, Emily Horne'

class ComicCrawler(BaseComicCrawler):
    def _get_url(self):
        self.parse_feed('http://www.rsspect.com/rss/asw.xml')

        for entry in self.feed.entries:
            if (self.timestamp_to_date(entry.updated_parsed) == self.pub_date
                and entry.link != 'http://www.asofterworld.com'):
                self.title = entry.title
                pieces = entry.summary.split('"')
                for i, piece in enumerate(pieces):
                    if piece.count('src='):
                        self.url = pieces[i + 1]
                    if piece.count('title='):
                        self.text = pieces[i + 1]
                    if self.url and self.text:
                        return
