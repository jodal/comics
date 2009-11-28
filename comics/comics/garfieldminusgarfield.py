from comics.crawler.base import BaseComicCrawler
from comics.meta.base import BaseComicMeta

class ComicMeta(BaseComicMeta):
    name = 'Garfield minus Garfield'
    language = 'en'
    url = 'http://garfieldminusgarfield.tumblr.com/'
    history_capable_days = 30
    schedule = 'Mo,Tu,We,Th,Fr'
    time_zone = -4
    rights = 'Travors'

class ComicCrawler(BaseComicCrawler):
    def _get_url(self):
        self.parse_feed('http://garfieldminusgarfield.tumblr.com/rss')

        for entry in self.feed.entries:
            if self.timestamp_to_date(entry.updated_parsed) == self.pub_date:
                pieces = entry.summary.split('"')
                for i, piece in enumerate(pieces):
                    if piece.count('src='):
                        self.url = pieces[i + 1]
                        return
